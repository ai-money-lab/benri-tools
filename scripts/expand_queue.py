#!/usr/bin/env python3
"""X投稿キューを大量追加するスクリプト（1回限り）"""
import json, os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
QUEUE_PATH = os.path.join(BASE_DIR, 'data', 'x_post_queue.json')

with open(QUEUE_PATH, 'r', encoding='utf-8') as f:
    queue = json.load(f)

new_posts = [
    {
        "id": "post_21_72rule",
        "body": "投資の「72の法則」知ってる？\n\n72 ÷ 利回り ＝ 資産が2倍になる年数\n\n年利3% → 24年\n年利5% → 14.4年\n年利7% → 10.3年\n年利10% → 7.2年\n\n銀行預金（0.01%）だと7,200年かかる。\n\n複利の力を知ってるかどうかで人生変わる。",
        "reply": "複利計算シミュレーターで確かめてみて\nhttps://ai-money-lab.github.io/benri-tools/compound-interest/"
    },
    {
        "id": "post_22_nenshu500",
        "body": "年収500万円の人が知るべき数字：\n\n手取り → 約390万（月32.5万）\n所得税 → 約14万\n住民税 → 約24万\n社会保険 → 約72万\n\n税金+社会保険で年間110万円取られてる。\n\nこれ知った上で「年収500万で十分」って言えるか考えてみて。",
        "reply": "自分の年収で正確に計算できます\nhttps://ai-money-lab.github.io/benri-tools/salary-calculator/"
    },
    {
        "id": "post_23_sim_switch",
        "body": "格安SIMに変えるだけで年6万円浮く。\n\n大手キャリア月7,000円\n格安SIM月2,000円\n差額：月5,000円 × 12ヶ月 = 6万円\n\n10年で60万円。\nその60万をNISAで運用すれば10年後に約78万円。\n\n何もしないことが一番高くつく。",
        "reply": "格安SIM13社の最新料金を毎日更新中\nhttps://ai-money-lab.github.io/benri-tools/sim-comparison/"
    },
    {
        "id": "post_24_kinri",
        "body": "住宅ローン金利が0.5%上がるだけで：\n\n借入4,000万・35年の場合\n0.5% → 月10.4万（総返済4,360万）\n1.0% → 月11.3万（総返済4,740万）\n1.5% → 月12.2万（総返済5,140万）\n\n0.5%の差で総額380万変わる。\n\n金利が低い今のうちに計算しておこう。",
        "reply": "住宅ローンシミュレーターはこちら\nhttps://ai-money-lab.github.io/benri-tools/loan-calculator/"
    },
    {
        "id": "post_25_sp500",
        "body": "S&P500に月5万円を20年積み立てた場合：\n\n年利7%想定\n元本：1,200万円\n運用益：+1,404万円\n合計：2,604万円\n\n元本の2倍以上になる。\n\nでもこれ、あくまで平均。リーマンショック級の暴落もある。\n\n自分のリスク許容度、確認してる？",
        "reply": "積立シミュレーションはこちら\nhttps://ai-money-lab.github.io/benri-tools/nisa-simulator/"
    },
    {
        "id": "post_26_furusato2",
        "body": "ふるさと納税やらない理由No.1：\n\n「よくわからないから」\n\n実際やることは3つだけ：\n1. 上限額を計算する\n2. 好きな返礼品を選んで寄附する\n3. 確定申告orワンストップ申請する\n\nたったこれだけで実質2,000円で数万円の返礼品がもらえる。",
        "reply": "上限額の計算はここで1分でできます\nhttps://ai-money-lab.github.io/benri-tools/furusato-tax/"
    },
    {
        "id": "post_27_hoken2",
        "body": "日本人の生命保険料の平均：\n\n月額約3.2万円（年間38万円）\n\n30歳から60歳まで払い続けると1,140万円。\n\nこれ、NISAで運用してたら約2,000万円になってる。\n\n保険は「必要な分だけ」が鉄則。\n入りすぎてる保険、今すぐ見直した方がいい。",
        "reply": "本当に必要な保障額を計算してみて\nhttps://ai-money-lab.github.io/benri-tools/insurance-calculator/"
    },
    {
        "id": "post_28_fx",
        "body": "FXで「月10万稼ぎたい」と思ってる人へ。\n\nまず計算してほしい。\n\n1ロット（1万通貨）でドル円が1円動くと：\n利益 → +10,000円\n損失 → -10,000円\n\nレバレッジ25倍なら必要証拠金は約6万円。\n\nリスクを数字で把握してからやらないと退場する。",
        "reply": "FX損益シミュレーターで計算してみて\nhttps://ai-money-lab.github.io/benri-tools/fx-calculator/"
    },
    {
        "id": "post_29_rougo",
        "body": "老後2000万円問題の正体：\n\n月の生活費25万 - 年金15万 = 毎月10万不足\n10万 × 12ヶ月 × 20年 = 2,400万円\n\nでもこれ「平均」の話。\n\n自分の場合いくら必要か、ちゃんと計算した方がいい。",
        "reply": "老後資金シミュレーターで計算できます\nhttps://ai-money-lab.github.io/benri-tools/retirement-fund/"
    },
    {
        "id": "post_30_tenshoku",
        "body": "転職で年収100万アップ！\n\n…でも手取りは70万しか増えない。\n\n年収400万→500万の場合：\n手取り315万→390万（+75万）\n\n年収800万→900万の場合：\n手取り590万→650万（+60万）\n\n高年収ほど税金が重い。\n転職前に「手取りベース」で判断する習慣をつけよう。",
        "reply": "年収別の手取り額を計算できます\nhttps://ai-money-lab.github.io/benri-tools/salary-calculator/"
    },
    {
        "id": "post_31_taishoku2",
        "body": "退職金の税金、勤続年数で全然違う：\n\n勤続20年 → 800万円まで非課税\n勤続30年 → 1,500万円まで非課税\n勤続35年 → 1,850万円まで非課税\n\n退職金2,000万で勤続20年の場合：\n課税対象 → 600万円\n税金 → 約90万円\n\n手取り1,910万円。思ったより取られる。",
        "reply": "退職金の手取りを正確に計算\nhttps://ai-money-lab.github.io/benri-tools/retirement-calculator/"
    },
    {
        "id": "post_32_fudousan2",
        "body": "ワンルームマンション投資の現実：\n\n物件2,500万・家賃9万/月\n表面利回り → 4.3%\n\nここから引かれるもの：\n管理費 -1万\n修繕積立 -0.8万\n固定資産税 -0.5万/月\n空室リスク -0.9万/月\n\n実質利回り → 2.3%\n\n表面利回りだけ見て買うと詰む。",
        "reply": "実質利回りを正確に計算できます\nhttps://ai-money-lab.github.io/benri-tools/real-estate-yield/"
    },
    {
        "id": "post_33_shitsugyo2",
        "body": "意外と知られてない失業保険の事実：\n\n・会社都合退職なら待機7日で即給付\n・自己都合は2ヶ月待ち（+7日）\n・45歳以上で勤続20年なら最大330日\n・再就職手当は残日数の60〜70%\n\n早く再就職すると「再就職手当」がもらえる。\n辞める前にシミュレーションしておこう。",
        "reply": "失業保険の受給額を計算できます\nhttps://ai-money-lab.github.io/benri-tools/unemployment-benefit/"
    },
    {
        "id": "post_34_nenkin2",
        "body": "年金の繰り下げ受給、知ってる？\n\n65歳から → 月15万円\n70歳から → 月21.3万円（+42%）\n75歳から → 月27.6万円（+84%）\n\n5年待つだけで月6万円増える。\n年間72万円の差。\n\nただし70歳まで生活費をどうするかが問題。",
        "reply": "年金受給額と必要貯金額を計算\nhttps://ai-money-lab.github.io/benri-tools/pension-calculator/"
    },
    {
        "id": "post_35_ievsyachin2",
        "body": "「家賃がもったいない」は本当か？\n\n家賃10万 × 35年 = 4,200万\n\nでも持ち家にも見えないコストがある：\n・固定資産税（年15万×35年=525万）\n・修繕費（35年で500万〜）\n・住宅ローン利息（数百万）\n\n「家賃を払い続けるのは無駄」は半分正解で半分ウソ。",
        "reply": "自分の条件で持ち家vs賃貸を比較\nhttps://ai-money-lab.github.io/benri-tools/rent-vs-buy/"
    },
    {
        "id": "post_36_haitou2",
        "body": "配当金投資を始めるなら覚えておくべき数字：\n\n配当利回り3%の株を100万円分買うと\n年間配当 → 3万円（税引前）\n税引後 → 約2.4万円\n月にすると → 2,000円\n\n「少ない」と感じたらNISAを使え。\n非課税なら年間3万円まるごと受け取れる。",
        "reply": "配当金シミュレーターで計算してみて\nhttps://ai-money-lab.github.io/benri-tools/dividend-yield/"
    },
    {
        "id": "post_37_ai2",
        "body": "AIで月5万の副業を作る方法：\n\n1. 便利なツールをAIに作らせる\n2. 無料公開してアクセスを集める\n3. 関連する商品のアフィリエイトを貼る\n\n自分がやったこと：\n・Claude AIにツール18個作らせた\n・月間PVが徐々に増加中\n\nポイントは「売る」より「役に立つ」を先にやること。",
        "reply": "作ったツールはこちら（全部無料）\nhttps://ai-money-lab.github.io/benri-tools/"
    },
    {
        "id": "post_38_kakutei2",
        "body": "確定申告で「経費」にできるもの：\n\n副業の場合：\n・PC購入費（10万円未満は全額OK）\n・通信費（仕事使用分）\n・書籍・教材費\n・交通費\n・サーバー代\n\n「経費を引く前」と「引いた後」で税金が全然違う。\n\n知らないだけで損してる人、めちゃくちゃ多い。",
        "reply": "税金計算シミュレーターはこちら\nhttps://ai-money-lab.github.io/benri-tools/tax-calculator/"
    },
    {
        "id": "post_39_nisa2",
        "body": "新NISAの「つみたて投資枠」と「成長投資枠」の使い方：\n\nつみたて枠（年120万）→ インデックス投信\n成長投資枠（年240万）→ 高配当株 or 投信\n\n合計年360万、生涯1,800万円まで非課税。\n\nまだ始めてない人、1日でも早い方がいい。",
        "reply": "NISAシミュレーターで計算してみて\nhttps://ai-money-lab.github.io/benri-tools/nisa-simulator/"
    },
    {
        "id": "post_40_fire2",
        "body": "サイドFIREという選択肢：\n\n完全FIREは7,500万円必要（月25万の場合）\n\nでもサイドFIRE（半分働く）なら：\n月12.5万を資産から + 月12.5万を労働で\n必要資産 → 3,750万円\n\n月10万を年利5%で20年積み立てると約4,110万円で達成。\n\n現実的じゃない？",
        "reply": "FIRE達成シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/retirement-fund/"
    },
    {
        "id": "post_41_sim2",
        "body": "「格安SIMは通信が遅い」\n\nこれ、もう嘘。\n\nahamo → 下り85Mbps\nUQモバイル → 下り72Mbps\nワイモバイル → 下り68Mbps\n\nYouTube 4K再生に必要な速度：25Mbps\n\n十分すぎる。まだ大手キャリアに月7,000円払ってるの？",
        "reply": "最新の料金比較はこちら\nhttps://ai-money-lab.github.io/benri-tools/sim-comparison/"
    },
    {
        "id": "post_42_loan2",
        "body": "住宅ローンの繰上返済、100万円でどれだけ変わるか：\n\n借入3,000万・金利1.0%・35年の場合\n\n5年目に100万繰上返済すると：\n→ 利息削減額：約32万円\n→ 返済期間：1年2ヶ月短縮\n\n15年目だと利息削減は約18万円。\n\n早ければ早いほど効果が大きい。",
        "reply": "繰上返済シミュレーション\nhttps://ai-money-lab.github.io/benri-tools/loan-calculator/"
    },
    {
        "id": "post_43_tedori2",
        "body": "ボーナスの手取り、思ったより少なくない？\n\nボーナス50万円の場合：\n健康保険 → -2.5万\n厚生年金 → -4.6万\n雇用保険 → -0.3万\n所得税 → -5.1万\n\n手取り → 約37.5万円（75%）\n\n25%引かれてる。\nボーナス100万なら25万消えてる。",
        "reply": "正確な手取り計算はこちら\nhttps://ai-money-lab.github.io/benri-tools/salary-calculator/"
    },
    {
        "id": "post_44_fukuri2",
        "body": "「貯金」と「投資」の30年後の差：\n\n毎月3万円を30年間：\n\n貯金（0.01%）→ 1,081万円\n投資（3%）→ 1,748万円\n投資（5%）→ 2,497万円\n投資（7%）→ 3,660万円\n\n同じ3万円でも置き場所で2,500万円の差。\n\nお金に働いてもらう意味、わかった？",
        "reply": "自分の条件で複利計算してみて\nhttps://ai-money-lab.github.io/benri-tools/compound-interest/"
    },
    {
        "id": "post_45_fx2",
        "body": "FX初心者が最初に知るべきこと：\n\n・1ロット（1万通貨）のUSD/JPY\n・レバレッジ25倍\n・必要証拠金 → 約6万円\n\nこれで1円動くと1万円の損益。\n\n「6万円で1万円稼げる！」\nと思った人、逆に1万円失う可能性も同じ。\n\nまず計算してからやろう。",
        "reply": "FX損益計算シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/fx-calculator/"
    },
    {
        "id": "post_46_tax_return2",
        "body": "確定申告が必要な人チェックリスト：\n\n□ 副業の所得が20万円超\n□ 2ヶ所以上から給与がある\n□ 医療費が10万円超\n□ ふるさと納税6自治体以上\n□ 住宅ローン控除1年目\n\n1つでも当てはまったら申告必要かも。\n30秒で判定できるチェッカー作った。",
        "reply": "確定申告チェッカーはこちら\nhttps://ai-money-lab.github.io/benri-tools/tax-return-checker/"
    },
    {
        "id": "post_47_toushi2",
        "body": "「投資は怖い」という人に見てほしい数字：\n\nS&P500の過去実績：\n1年 → -37%〜+53%（振れ幅大）\n10年 → -1%〜+20%（ほぼプラス）\n20年 → +6%〜+17%（マイナスなし）\n\n短期は怖い。でも長期なら話が変わる。\n\n大事なのは「長く続けること」。",
        "reply": "投資リターンを計算してみて\nhttps://ai-money-lab.github.io/benri-tools/investment-return/"
    },
    {
        "id": "post_48_ai3",
        "body": "Claude AIでツールを作る手順：\n\n1. 「○○計算機をHTMLで作って」と指示\n2. 出力されたコードをファイルに保存\n3. GitHub Pagesで無料公開\n\n以上。\n\nプログラミング知識ゼロで18個作った。\n\n「AIは使い方がわからない」\nこれ、使わない理由にはならない。",
        "reply": "作ったツール一覧はこちら\nhttps://ai-money-lab.github.io/benri-tools/"
    },
    {
        "id": "post_49_nenshu300",
        "body": "年収300万でも資産は作れる：\n\n手取り → 月約20万\n生活費 → 月15万（倹約）\n投資 → 月5万\n\n月5万 × 年利5% × 20年 = 2,055万円\n\n年収が低くても「仕組み」を作れば資産は増える。\n\n大事なのは収入じゃなく「収入-支出」の差額。",
        "reply": "年収別の手取りと投資シミュレーション\nhttps://ai-money-lab.github.io/benri-tools/salary-calculator/"
    },
    {
        "id": "post_50_haitou3",
        "body": "高配当株の「罠」：\n\n配当利回り7%の株、魅力的に見えるけど…\n\n・業績悪化で減配リスクあり\n・株価下落で元本割れ\n・高利回り＝市場が警戒してる証拠\n\n健全な高配当の目安は3〜5%。\n利回りだけでなく配当性向もチェックしよう。",
        "reply": "配当金シミュレーターで計算\nhttps://ai-money-lab.github.io/benri-tools/dividend-yield/"
    },
    {
        "id": "post_51_nenkin3",
        "body": "フリーランスの年金、会社員の半分以下：\n\n会社員（年収500万・30年）→ 月約17万\nフリーランス（30年）→ 月約6.5万\n\n差額：月10万 × 30年 = 3,600万\n\nフリーランスは自分で備えないと老後詰む。\niDeCoとNISAの併用が最低ライン。",
        "reply": "年金受給額を計算\nhttps://ai-money-lab.github.io/benri-tools/pension-calculator/"
    },
    {
        "id": "post_52_ie3",
        "body": "持ち家のメリットを数字で見ると：\n\n住宅ローン控除（13年間）→ 最大455万円の減税\n団信 → 死亡時にローン残債ゼロ\n老後 → 家賃負担なし\n\nデメリット：\n転勤リスク・修繕費・固定資産税\n\nどっちが得かは「条件次第」。\n感覚じゃなく数字で判断しよう。",
        "reply": "持ち家vs賃貸シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/rent-vs-buy/"
    },
    {
        "id": "post_53_furusato3",
        "body": "ふるさと納税の実質還元率：\n\nお米 → 還元率30%以上\n牛肉 → 還元率25〜30%\n海鮮 → 還元率20〜25%\n\n年収500万・独身の上限約6万円を全部お米にすると約20kgのお米が届く。\n\n食費が月2,000円浮く計算。やらない理由がない。",
        "reply": "自分の上限額を計算\nhttps://ai-money-lab.github.io/benri-tools/furusato-tax/"
    },
    {
        "id": "post_54_shitsugyo3",
        "body": "知ってた？失業保険をもらいながら：\n\n・アルバイトOK（週20時間未満）\n・スキルアップ訓練に通える（交通費支給）\n・訓練中は給付延長される場合あり\n\n「辞めたら収入ゼロ」じゃない。\n\nでも自己都合退職は2ヶ月待ちだから、その間の生活費は用意しておこう。",
        "reply": "失業保険の金額を計算\nhttps://ai-money-lab.github.io/benri-tools/unemployment-benefit/"
    },
    {
        "id": "post_55_fudousan3",
        "body": "不動産投資で「キャッシュフロー」が出るかの計算：\n\n家賃8万 - ローン返済5万 - 管理費1.5万 - 修繕0.8万 - 固定資産税0.4万\n= 月0.3万円（年3.6万円）\n\n空室が2ヶ月出たら年間マイナス。\n\n「不労所得」の幻想、数字で見ると目が覚める。",
        "reply": "不動産利回りを正確に計算\nhttps://ai-money-lab.github.io/benri-tools/real-estate-yield/"
    },
    {
        "id": "post_56_ai_tools",
        "body": "「プログラミングを勉強しなきゃ」\n\nと思ってる人、ちょっと待って。\n\nAIに頼めば：\n・計算ツール → 5分で完成\n・比較表 → データ入れれば自動生成\n・Webサイト → 指示するだけ\n\n「作る力」より「指示する力」の時代。\n\n実際に18個作った自分が言うから間違いない。",
        "reply": "AIで作ったツール一覧\nhttps://ai-money-lab.github.io/benri-tools/"
    },
    {
        "id": "post_57_loan3",
        "body": "住宅ローン「変動」vs「固定」：\n\n変動（0.5%）→ 月10.4万\n固定（1.8%）→ 月12.9万\n差額 → 月2.5万（年30万）\n\n35年で1,050万の差。\n\nでも変動金利が2%に上がったら逆転する。\n「今安い」だけで選ぶと将来痛い目に遭うかも。",
        "reply": "金利別のシミュレーション\nhttps://ai-money-lab.github.io/benri-tools/loan-calculator/"
    },
    {
        "id": "post_58_tsumitate",
        "body": "積立投資の「ドルコスト平均法」の威力：\n\n毎月3万円を投資した場合：\n株価が下がった月 → 多く買える\n株価が上がった月 → 少なく買う\n\n結果、平均取得単価が下がる。\n\n一括投資と違って「いつ始めても正解」になりやすい。\nだからNISAは「今すぐ始める」が最適解。",
        "reply": "積立シミュレーション\nhttps://ai-money-lab.github.io/benri-tools/nisa-simulator/"
    },
    {
        "id": "post_59_tax2",
        "body": "会社員でも節税できること一覧：\n\n・ふるさと納税（全員OK）\n・iDeCo（掛金が全額控除）\n・医療費控除（10万超）\n・住宅ローン控除（最大455万）\n・生命保険料控除（最大12万）\n\n何もしないと毎年数万〜数十万円損してる。\nまず自分の税金がいくらか知ることから。",
        "reply": "税金計算ツール\nhttps://ai-money-lab.github.io/benri-tools/tax-calculator/"
    },
    {
        "id": "post_60_hoken3",
        "body": "医療保険、本当に必要？\n\n日本は高額療養費制度があるから：\n年収500万の場合、月の自己負担上限 → 約8万円\n\nつまり入院しても月8万で済む。\n\n医療保険に月3,000円払い続けると30年で108万円。\n\n「もしもの8万円」のために108万払う？\n計算してから決めよう。",
        "reply": "必要保障額を計算\nhttps://ai-money-lab.github.io/benri-tools/insurance-calculator/"
    },
    {
        "id": "post_61_nenshu_real",
        "body": "「年収1,000万は勝ち組」の幻想：\n\n手取り → 約720万（月60万）\n\n東京で家族4人：\n家賃15万+食費10万+教育費8万+保険3万+車2万+その他10万 = 月48万\n\n貯蓄 → 月12万\n\n意外とカツカツ。\n年収より「支出の最適化」が大事。",
        "reply": "年収別の手取り計算\nhttps://ai-money-lab.github.io/benri-tools/salary-calculator/"
    },
    {
        "id": "post_62_toushi3",
        "body": "投資の名言を数字で検証：\n\n「卵を一つのカゴに盛るな」\n\n全額を株式 → 年リターン7%（暴落時-40%）\n株60:債券40 → 年リターン5%（暴落時-20%）\n\n分散するとリターンは下がるが暴落に耐えやすくなる。\n自分に合うバランスを見つけよう。",
        "reply": "投資リターン計算機\nhttps://ai-money-lab.github.io/benri-tools/investment-return/"
    },
    {
        "id": "post_63_fx3",
        "body": "FXの「スワップポイント」で稼ぐ方法：\n\n高金利通貨を買って保有するだけで毎日利息がもらえる。\n\nメキシコペソ/円：1万通貨で約20円/日\n10万通貨なら200円/日 = 月6,000円\n\nただし為替変動リスクあり。\n1円動くと±10万円。スワップ狙いでもリスク管理は必須。",
        "reply": "FX損益シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/fx-calculator/"
    },
    {
        "id": "post_64_compound3",
        "body": "「時間」が最大の武器である証拠：\n\n月3万円を年利5%で積み立てた場合：\n\n25歳から（40年）→ 4,580万円\n35歳から（30年）→ 2,497万円\n45歳から（20年）→ 1,233万円\n\n10年遅れるごとに1,000万円以上の差。\n投資は「いつ始めるか」が全て。",
        "reply": "複利計算シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/compound-interest/"
    },
    {
        "id": "post_65_taishoku3",
        "body": "iDeCoで退職金の税金を減らす方法：\n\n退職金とiDeCoは「退職所得控除」を共有する。\n\nただし受け取り方を工夫すれば：\n・iDeCoを60歳で一括受取\n・退職金を65歳で受取\n→ 控除枠を2回使える可能性あり\n\n受け取り順とタイミングで税金が数十万変わる。",
        "reply": "退職金の手取りシミュレーション\nhttps://ai-money-lab.github.io/benri-tools/retirement-calculator/"
    },
    {
        "id": "post_66_tools_18",
        "body": "毎日自動更新されるお金のツール集：\n\n格安SIM → 13社の料金を毎日収集\n税金計算 → 最新の税率に対応\n年金シミュ → 最新の年金制度に対応\n\n他にも18ツール、全部無料。\n\nブックマークしておけば、お金で迷ったときにすぐ答えが出る。",
        "reply": "全ツール一覧\nhttps://ai-money-lab.github.io/benri-tools/"
    },
    {
        "id": "post_67_fire3",
        "body": "FIRE達成者の共通点：\n\n1. 収入の50%以上を投資に回す\n2. 固定費を極限まで下げる\n3. インデックス投資を淡々と続ける\n4. 副業で収入源を増やす\n\n月25万で生活して月25万投資すると：\n年利5%で20年 → 約1億円\n\nFIREは「高収入」じゃなく「高貯蓄率」で決まる。",
        "reply": "FIRE達成シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/retirement-fund/"
    },
    {
        "id": "post_68_sim3",
        "body": "家族4人のスマホ代：\n\n大手キャリア → 月28,000円（年33.6万）\n格安SIM → 月8,000円（年9.6万）\n\n差額：年24万円\n10年で240万円。\n\nこの240万をNISAで運用すれば10年後300万超。\n格安SIMに変えるだけで「投資の原資」が生まれる。",
        "reply": "格安SIM比較表\nhttps://ai-money-lab.github.io/benri-tools/sim-comparison/"
    },
    {
        "id": "post_69_rougo2",
        "body": "定年後にかかるお金、甘く見てない？\n\n月の支出（夫婦2人）：\n食費7万+住居3万+光熱2万+医療3万+交通2万+娯楽3万+他5万\n合計：25万円/月\n\n年金15万だと毎月10万不足。\n65歳までにいくら貯めるべき？",
        "reply": "老後資金シミュレーター\nhttps://ai-money-lab.github.io/benri-tools/retirement-fund/"
    },
    {
        "id": "post_70_kakutei3",
        "body": "医療費控除、使ってない人多すぎ：\n\n年間の医療費が10万円超えたら確定申告で取り戻せる。\n\n対象：病院代・薬代・通院交通費・歯科・レーシック\n家族合算OK。\n\n年間15万かかってたら約1.5万円戻ってくる。",
        "reply": "税金計算ツールで控除額を確認\nhttps://ai-money-lab.github.io/benri-tools/tax-calculator/"
    },
]

queue.extend(new_posts)

with open(QUEUE_PATH, 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

total = len(queue)
posted = sum(1 for p in queue if p.get('posted', False))
remaining = total - posted
print(f'Queue updated: {total} total, {posted} posted, {remaining} remaining')
print(f'Estimated days of content: {remaining} days (~{remaining//30} months)')
