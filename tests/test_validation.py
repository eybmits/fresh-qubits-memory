"""Independent small cases for optional channel simulations."""

import importlib.util
import unittest

AVAILABLE = importlib.util.find_spec('numpy') is not None
if AVAILABLE:
    import numpy as np
    from fresh_qubits_memory.validation import (
        bit_channel, bound_constants, cooling_step, depolarize_density,
        repetition_permutation, repetition_step, reset_density,
    )


@unittest.skipUnless(AVAILABLE, 'optional validation dependencies not installed')
class ChannelValidationTests(unittest.TestCase):
    def test_partial_trace_reset_destroys_bell_correlations(self):
        bell=np.array([1,0,0,1])/np.sqrt(2)
        rho=np.outer(bell,bell)
        eta=np.array([[.5,.5j],[-.5j,.5]])
        got=reset_density(rho,eta,1)
        np.testing.assert_allclose(got,np.kron(eta,np.eye(2)/2),atol=1e-15)
        # Independent Kraus reset for an arbitrary entangled density matrix.
        v=np.array([1,-1j])/np.sqrt(2)
        expected=np.zeros((4,4),dtype=complex)
        for j in range(2):
            K=np.kron(np.outer(v,np.eye(2)[j]),np.eye(2))
            expected+=K@rho@K.conj().T
        np.testing.assert_allclose(got,expected,atol=1e-15)

    def test_depolarizing_against_independent_full_kraus_sum(self):
        rng=np.random.default_rng(192)
        z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        rho=z@z.conj().T;rho/=np.trace(rho)
        I=np.eye(2);X=np.array([[0,1],[1,0]])
        Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
        q=.63;weights=[(1+3*q)/4]+[(1-q)/4]*3
        expected=np.zeros_like(rho)
        for w,A in zip(weights,(I,X,Y,Z)):
            for u,B in zip(weights,(I,X,Y,Z)):
                K=np.kron(A,B)
                expected+=w*u*(K@rho@K.conj().T)
        np.testing.assert_allclose(depolarize_density(rho,q,2),expected,atol=1e-14)
        np.testing.assert_allclose(depolarize_density(rho,0,2),np.eye(4)/4,atol=1e-14)
        np.testing.assert_allclose(depolarize_density(rho,1,2),rho,atol=1e-14)

    def test_classical_channel_equals_quantum_diagonal_restriction(self):
        p=np.arange(1,9,dtype=float);p/=p.sum()
        np.testing.assert_allclose(bit_channel(p,3,.13,.87),np.diag(depolarize_density(np.diag(p),.74,3)),atol=1e-15)

    def test_single_copy_cycle_order_and_permutation(self):
        r=1;q=.8;perm=repetition_permutation(r)
        self.assertEqual(len(set(perm)),16)
        state=np.ones(16)/16
        z=1-2*(np.arange(16)&1)
        for t in range(6):
            state=repetition_step(state,r,q,int(t==0),1 if t==0 else 0,perm)
            self.assertAlmostEqual(float(z@state),-q**(t+1),places=13)

    def test_cooling_joint_count_transition_matches_bit_enumeration(self):
        # r=2, two blocks. At counts (1,2), threshold vote is 1.
        # XOR/rotation gives block counts (0,1); use representative 00|10.
        p=np.zeros(16);p[2]=1
        exact=bit_channel(p,4,.05,.68)
        expected=np.zeros((3,3))
        for label,prob in enumerate(exact):
            expected[(label>>2).bit_count(),(label&3).bit_count()]+=prob
        trials=150_000
        states=np.tile([1,2],(trials,1))
        sampled=cooling_step(states,2,.9,.3,np.random.default_rng(993))
        counts=np.zeros((3,3))
        np.add.at(counts,(sampled[:,0],sampled[:,1]),1)
        sigma=np.sqrt(expected*(1-expected)/trials)
        self.assertTrue(np.all(np.abs(counts/trials-expected)<6*sigma+1/trials))

    def test_known_upper_constant(self):
        theta,logr,loginv=bound_constants(.5,1)
        self.assertAlmostEqual(theta,.4)
        self.assertAlmostEqual(loginv,11.)


if __name__=='__main__':
    unittest.main()
