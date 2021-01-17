# Health Planet Data Tool
## What is this?
- タニタのHealth planetから体組成計の計測データをエクスポートします。
- タニタのAPIを叩いて取得するので、クライアントアプリケーション登録を予め準備する必要があります。（後述参照）

## 実行環境
### 必須
- python3.7かそれ以上
### できたら
- venv
    - 勝手に`venv`ディレクトリを作成させていただきます。

## setup
### Client ID / Client secretの取得
- HealthPlanetのマイページ＞登録情報の確認・変更＞サービス連携＞アプリケーション開発者の方はこちら
- 上記の経路で、APIの設定を完了することで取得可能
### `run.sh`の編集
```
LOGIN_ID: HealthPlanetのユーザID
CLIENT_ID: 先程取得したClient ID
CLIENT_SECRET: 先ほど取得したClient secret
CHECK_EXISTS_VENV: venvを使うときはtrue, 使わないまたは自前のときはfalse
FROM_DATE: `YYYYmmdd`形式で指定可能（TO_DATEより前の日付を指定）または`today`で84日前（28*3）を指定可能
TO_DATE: `YYYYmmdd`形式で指定可能（FROM_DATEより後の日付を指定）または`today`で現在時刻を指定可能
OUT_FILE: 出力ファイルのパスを指定（拡張子はjsonを推奨）
```
### venvを使用しない方はもう1ステップ
```
python3 -m pip install -r requirements.txt
# または
pip install -r requirements.txt
```

## 実行
- 注意：途中でHealthPlanetのパスワードを要求します。
```:sh
sh run.sh
> Please enter your password: (your password)
```

## 出力
- jsonデータ
```
{
    "birth_date": $誕生日,
    "height": $身長,
    "sex": $性別,
    "data": [
        {
            "date": $測定日,
            "keydata": $測定データ値,
            "model": $測定機器名,
            "tag": $測定部位
        }
    ]
}
```
- 測定部位の数値
    - `6021`：体重（kg）
    - `6022`：体脂肪率（%）
