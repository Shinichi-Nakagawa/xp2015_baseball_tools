# xp2015_baseball_tools
XP祭り2015「アジャイル脳によく効く野球のハナシ」に使ったツール

## 何が出来るの？

- 某Yahoo!の日本プロ野球順位表・個人成績からデータを抽出してExcel出力できます
    - 順位表+チーム成績
    - 個人成績（打者）
    - 【未対応】個人成績（投手）
- 抽出したデータと同時に、セイバーメトリクス指標も出力します。
    - ピタゴラス勝率（勝率、予想勝利、予想敗戦）
    - OPS
    - アダム・ダン率
    
## 使い方

- Python実行環境を準備
    - Python 3.4.x推奨(3.4.3で動作確認済み)
    - Python 2.xは未対応
    - brew install python3とかでインストールできます
    
- ライブラリをインストール

    pip install -r requirements.txt
    
- 実行
    - 順位表+チーム成績
    
        python npb_standings.py
    
    - 個人成績（打者）
        
        python npb_batter_stats.py

    - 個人成績（投手）
        
        python npb_pitcher_stats.py
        
    - 書籍「野球×統計は最強のバッテリーである」の指標を再現
    
        python example_npb_stats.py
