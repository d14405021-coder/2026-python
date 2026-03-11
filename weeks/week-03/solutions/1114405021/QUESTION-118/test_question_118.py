"""
單元測試：手工輸入版的 UVA 118 簡易程式

這個測試模組會呼叫 solution_118-easy-hand.py 中的 process_robot
函數，確保手打程式行為與簡易版相同。
"""

import unittest
import runpy
import os

# 透過 runpy 執行手寫版程式並取得 process_robot 函數
path = os.path.join(r'd:\21\2026-python\weeks\week-03\solutions\1114405021',
                    'solution_118-easy-hand.py')
namespace = runpy.run_path(path)
process_robot = namespace['process_robot']

class TestHandRobot(unittest.TestCase):
    def test_basic(self):
        scent = set()
        self.assertEqual(process_robot(0,0,'N','F',5,5,scent),(0,1,'N',False))

if __name__=='__main__':
    unittest.main()
