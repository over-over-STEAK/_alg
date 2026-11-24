# AI 使用：有，ChatGPT 協助撰寫。
import unittest
import q1_diff_int_1d
import q2_mc_1d
import q3_grad_integral_n
import q4_mc_n
import q5_riemann_n
import q6_mc_generic

class TestAll(unittest.TestCase):
    def test_q1(self):
        q1_diff_int_1d.test()
    def test_q2(self):
        q2_mc_1d.test()
    def test_q3(self):
        q3_grad_integral_n.test()
    def test_q4(self):
        q4_mc_n.test()
    def test_q5(self):
        q5_riemann_n.test()
    def test_q6(self):
        q6_mc_generic.test()

if __name__ == "__main__":
    unittest.main()
