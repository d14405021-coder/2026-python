# 題目 10170

**題名**: UVA 10170

> ⚠️ **>
> 【狀態】題目敘述、輸入說明、輸出說明待補充
>
> 【建議】請參考以下連結自行補充：
> - [ZeroJudge 題目頁面](https://zerojudge.tw/ShowProblem?problemid=a163)
> - [UVA Online Judge](https://uva.onlinejudge.org/external/10170.pdf)
> - [Yui Huang 題解參考](https://yuihuang.com/cpe-level-1/)

**相關連結**:
- [ZeroJudge 題目頁面](https://zerojudge.tw/ShowProblem?problemid=a163)
- [UVA Online Judge](https://uva.onlinejudge.org/external/10170.pdf)

## 題目敘述


此題涉及大數運算和模運算。
給定兩個整數 n 和 m，需要計算 n 的 m 次方對 10007 的模。
由於指數 m 可能非常大（高達 2^31-1），直接計算會導致整數溢出。
必須使用快速冪演算法（Binary Exponentiation）結合模運算來高效地求解。

## 輸入說明


輸入包含多個測試案例。
每行包含兩個整數 n 和 m（0 ≤ n, m ≤ 2^31-1）。
當 n 和 m 都為 0 時，輸入結束。

## 輸出說明


對於每個測試案例，輸出 (n^m) mod 10007 的結果。
由於使用了模運算，結果必然在 0 至 10006 之間。

## 解題思路

*請填入你的解題思路*

## 解題代碼

```python
# 你的代碼這裡
```

## 測試用例

*測試輸入與預期輸出*
