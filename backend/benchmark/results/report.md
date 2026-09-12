# STT Benchmark Report

Provider comparison on the clips listed in `clips/manifest.csv`.

## Macro-average WER / CER

| Language pair | sahara | groq | local_whisper |
| ha-en | 0.696 / 0.449 | 1.046 / 0.542 | 1.171 / 0.671 |
| ig-en | 0.619 / 0.299 | 0.554 / 0.360 | 1.149 / 0.584 |
| pcm-en | 0.357 / 0.246 | 0.518 / 0.413 | 0.672 / 0.441 |
| yo-en | 0.505 / 0.307 | 0.992 / 0.651 | 1.172 / 0.866 |

## Intent exact-match accuracy

Intent scores are evaluated on a small set of 6 real fintech utterances with expected intents.

| Language pair | sahara | groq | local_whisper |
| ha-en | 100.0% / 100.0% / 100.0% | 0.0% / 100.0% / 100.0% | 33.3% / 100.0% / 100.0% |
| ig-en | n/a | n/a | n/a |
| pcm-en | n/a | n/a | n/a |
| yo-en | 100.0% / 100.0% / 100.0% | 33.3% / 100.0% / 66.7% | 0.0% / 100.0% / 100.0% |

## Observed failure modes

### sahara

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual: [failure] Sahara transcription still processing after polling, file_id=080b7221-bfe3-4e86-b8c7-505e362c73b7
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual: Ẹ má bínú, ṣé mọ pé ọkùnrin ni mí and ọmọ Boys ní láti stroke law ọmọ bó sì jagunlo ni boys torí pé o jẹ́ ọmọ boys torí pé ó jẹ́ ọmọkùnrin náà ló ṣe fẹ́ pa ni

- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual: Bechool to make tí ó máa mú ẹ̀ dùn nìyẹn anywhere you are agreed by some committee thank you so much one tigbo ni now nǹkan tó máa ṣẹlẹ̀ ń sì ni pé tá máa fi rí

- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual: University kan lọ kọ́ bí ṣábọ̀ṣàn lọ́tọ̀ náà ni àdẹfẹ́yọ̀ wà láyé wà láyé common shift that

- `afriswitch/yoruba_04.wav`
  - Reference: Mi ko ma ran, ko ma ma mu oriburuku ko mi mu, lọ funrarẹ, Abi ki o ri gun, kii foriburuku yé na? ti mo bímọ tán kín ṣẹ ma wa ọmọ ti ma rent ko lọ bámi ra ọja wa? Ẹ̀bi rẹ kó. ṣe wọ lo lọmọ ni? ẹ sẹbi rẹ ṣẹ.
  - Actual: Mi rọ̀ kọ́ mú orí burúkú kọ mímú lọ fúnra rẹ̀ àbí kí ló rí gù kíríkú tí mo bímọ tán máa wé ọmọ tí màá rẹ́ǹtì kọ́ lọ bá mi ra ọjà wá ló ṣèbí

- `afriswitch/hausa_00.wav`
  - Reference: Ya ce haraje haraje na Amurka a kan tarayya Turai za su kara rura wutar kalubalen da nahiyar tiri ke fama da su a cewarsa yakin kasuwancin da donald trump ya kaddamar
  - Actual: 

- `afriswitch/hausa_01.wav`
  - Reference: Saboda yanzu abinda ake yi ana daukan yanzu kamar iskan gas cikon mota ana Taliya dashi
  - Actual: 

- `afriswitch/hausa_02.wav`
  - Reference: Don dole haka na zama mai bada shawara saboda haka har guri ne da nima yanzu duk wani mai matsala zai zo ya same ni ga matsalata ko macen ko namiji to
  - Actual: Karin gwiwa shaida mana

- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual: 

- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual: Allah

- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual: Ọ kelekwere ọ kelekwere ọ kelesi remember we share this

- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: Pastọ ka ị kpechaa kpechaa, yor mee na full

- `clips/fintech_recorded/ha_07.wav`
  - Reference: Lambar asusuna
  - Actual: Lambar asusu na

### groq

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual:  ਹੋ ੫३, ੧१, ਹ੒,੩,੩.
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual:  Ƥe ma binu ʃe mokun ʉi nimi. ƒ əmò mò ʉo wǒi səm əlati ə ʉi ʍrò wǒu lò wə. ƒ mò ʉo wǒi si ʉi ʉi ʉi kŏgু lòni. ƈò mò wǒi. ƈò rì kò ʉi ʉi ʎmò wǒi. ʈè rì ʉi ʉi ʉi kò ʉi ʉi ʉi ʉi ʐò mò ʉi nini ʉi ʈi ʉi ʉi ʉi ʉi.
- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual:  Thank you so much! Tio wana ti bwona ebay. Ora mi gidiki goni. Now, nkoto ma shell lens e pe, ta ma fiuri
- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual:  Pisha chibu losi investi kon lo, komo jen shi abo shi on loto. O deno on ya defe, on yu de yo, o wolo de wala ye, lo wala ye. Come on, ship that to your daughter.
- `afriswitch/yoruba_04.wav`
  - Reference: Mi ko ma ran, ko ma ma mu oriburuku ko mi mu, lọ funrarẹ, Abi ki o ri gun, kii foriburuku yé na? ti mo bímọ tán kín ṣẹ ma wa ọmọ ti ma rent ko lọ bámi ra ọja wa? Ẹ̀bi rẹ kó. ṣe wọ lo lọmọ ni? ẹ sẹbi rẹ ṣẹ.
  - Actual:  Mi koma wamu o li buruku komi mu, lafura le, abiki li o li gubi ki li buruku ye na. E ti mobi mata kense ma wawo, mo ti ma renti koloba mera o jawan. Che walo lomoni? E shebi rese.
- `afriswitch/hausa_00.wav`
  - Reference: Ya ce haraje haraje na Amurka a kan tarayya Turai za su kara rura wutar kalubalen da nahiyar tiri ke fama da su a cewarsa yakin kasuwancin da donald trump ya kaddamar
  - Actual:  Esa va savo cande ea cora conterra e cua est, ca ola ea cora ea cora ea cora, ca ola ea cora ea cora, et si ea sae aca, et si ea sae aca, et si ea sae aca,
- `afriswitch/hausa_01.wav`
  - Reference: Saboda yanzu abinda ake yi ana daukan yanzu kamar iskan gas cikon mota ana Taliya dashi
  - Actual:  S'il vous a plaitit, vous m'accrochez, En avant de vous, A ce que vous exprimiez de votre chasse.
- `afriswitch/hausa_02.wav`
  - Reference: Don dole haka na zama mai bada shawara saboda haka har guri ne da nima yanzu duk wani mai matsala zai zo ya same ni ga matsalata ko macen ko namiji to
  - Actual:  Kari Deva, the Kama Salyamata Saurasa, the Kari Deva Rata Nila, the Zaddiya Namaya Samajna Sattva Namaka Vassalata, the Murechi Yama Yaji, K.
- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual:  Mereka meraka merasa meraka. Meraka meraka meraka. Meraka meraka meraka.
- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual:  Son of our action, watch out. Lose that to a considerable intruder. I can tell you so. I make you a character with incredible affection. Hello. I like to turn over a show. I'm a cautious luncheon
- `afriswitch/pidgin_03.wav`
  - Reference: Na the okal predo na e go call because like no people talk the bug stop satis stable So e must work round the drug to use enckure say make nobody cause am embarrassment and make nobody spoil him name
  - Actual:  ਸੈ ਸੋਸੀ ਸੋਸੀ ਸੋਸੀ
- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual:  oh
- `clips/fintech_recorded/yo_01.wav`
  - Reference: Wo èyí tó kù nínú àkántì mi
  - Actual:  Uyitoku nunu akaundzimi.
- `clips/fintech_recorded/yo_02.wav`
  - Reference: Kí ni àkántì nómba?
  - Actual:  Kini account nomba mi.
- `clips/fintech_recorded/yo_03.wav`
  - Reference: Mo fẹ́ gba owó mi.
  - Actual:  Mufet Baumi
- `clips/fintech_recorded/yo_04.wav`
  - Reference: Mo fẹ́ fi owó ránṣẹ́ sí…
  - Actual:  Mufafi, orang asyik nasi
- `clips/fintech_recorded/yo_05.wav`
  - Reference: Àkántì nómba wo ló fẹ́ fi owó ránṣẹ́ sí?
  - Actual:  Account number will offer free OUO Noshesi.
- `clips/fintech_recorded/yo_06.wav`
  - Reference: Báńkì wo ló fẹ́ fi owó ránṣẹ́ sí?
  - Actual:  Banki wo luphe fi owono chensi.
- `clips/fintech_recorded/yo_07.wav`
  - Reference: Mo fẹ́ fi 500 naira ránṣẹ́ sí àkántì nómba wán yìí, 7011334637. Ṣé kì n tẹ̀ síwájú?
  - Actual:  Mofe fi 500 nera lon shesi account nomba onyi 7011334637. She, Kintesi Waju.
- `clips/fintech_recorded/yo_08.wav`
  - Reference: Ẹ̀san wo rè tí ṣe yọrí?
  - Actual:  You saw already, Shiori?
- `clips/fintech_recorded/ha_01.wav`
  - Reference: Ina so in cire kuɗi na
  - Actual:  ជំល្រូប្រំពីពាច្នឹងដែម
- `clips/fintech_recorded/ha_02.wav`
  - Reference: tura kuɗin ya tafi cikin nasara
  - Actual:  Tu răcur în iata fiice, gândoasele.
- `clips/fintech_recorded/ha_04.wav`
  - Reference: Ina so in tura kuɗi ma .....
  - Actual:  Inasun Tulekut Ima
- `clips/fintech_recorded/ha_05.wav`
  - Reference: Ina son in duba account balance ɗina
  - Actual:  Ini asal dua bahagian balas dina.
- `clips/fintech_recorded/ha_06.wav`
  - Reference: Wace bank za a tura
  - Actual:  Wachibang za atura.
- `clips/fintech_recorded/ha_07.wav`
  - Reference: Lambar asusuna
  - Actual:  Lama Azizuna
- `clips/fintech_recorded/ha_08.wav`
  - Reference: Ina so in tura dari biyar(₦500) zuwa wannan account numba, dede ne?
  - Actual:  Ina soturet ribia rizua wana account number dedene.
### local_whisper

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual: Quand tu a conchamé, mais non, quand c'est bon, c'est qu'on n'a pas complisement. Sur la dizaine, il m'allait m'achicher, mais à la vraie chôpe de ma fère, c'est ce que tu veux. Tu veux que tu veux, non, c'est vrai. Mais je vais te faire.
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual: Perna, vi non c'è mapei o con l'animi Ando ma voice in l'acestrogo di ormigli Oma voice di jabi non è Ovo voice? Poi non puoi giamo a voice? Eh? Si è toli po' di omo puri non lui si fai a pally?
- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual: Ben, I'm sorry, I'm going to talk to my mom. I don't need it. I don't need it. I'm going to talk to my mom. Oh, sure. It's so cold. Thank you so much. That's fine, I'm fine. Now, I'm getting a gun. Ah. Now, I'm going to talk to my parents. I'm fine. I'm fine.
- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual: Gizache was a must come on CPCB. ということは、どんなようにできるようです。 国安の壊らない、聞こえます。 もし、知ったものを言うと、 その時は、 最後の国は、 新しい水・食物が提価します。 君が、 私の私も食物を聞こえるのもあります。 私は、 私は食物を聞いています。 私は、 私は私は食物を聞こえるのも、
- `afriswitch/yoruba_04.wav`
  - Reference: Mi ko ma ran, ko ma ma mu oriburuku ko mi mu, lọ funrarẹ, Abi ki o ri gun, kii foriburuku yé na? ti mo bímọ tán kín ṣẹ ma wa ọmọ ti ma rent ko lọ bámi ra ọja wa? Ẹ̀bi rẹ kó. ṣe wọ lo lọmọ ni? ẹ sẹbi rẹ ṣẹ.
  - Actual: Mey, Kamala, Kamala, Kamala, Mahmoudi, Pruku, Kamemo, Lafurale, Abkhirani, Kamekir Puri, Puku, Yena. Ezimobi, Madhaktin, Zehmao, Mahmoudi, Mahrenti, Kola, Mahmoudi, Dawa. Tevalo, Laman. Eh, Shabirase. Ah!
- `afriswitch/hausa_00.wav`
  - Reference: Ya ce haraje haraje na Amurka a kan tarayya Turai za su kara rura wutar kalubalen da nahiyar tiri ke fama da su a cewarsa yakin kasuwancin da donald trump ya kaddamar
  - Actual: From her, from her, from her, from her of--" From her. Have thehanthus be shared? A changes in my heart. And I look over shouting.
- `afriswitch/hausa_01.wav`
  - Reference: Saboda yanzu abinda ake yi ana daukan yanzu kamar iskan gas cikon mota ana Taliya dashi
  - Actual: Ashen-Am fai-Am Fai-Am I'm just a brat Ashen-Am I'm just pretty Fai-Am
- `afriswitch/hausa_02.wav`
  - Reference: Don dole haka na zama mai bada shawara saboda haka har guri ne da nima yanzu duk wani mai matsala zai zo ya same ni ga matsalata ko macen ko namiji to
  - Actual: Are you going to call us a regular guard? La la la la la la!
- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual: [empty transcript]
- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual: Schöner auf Wachfahrt, Löcher zur Träckshörde, Er bin von dem Akkante, Schöner, Er bin der Tavelkön, Er bin der Tavelkön, Er bin der Tavelkön, Für die Faltwarte von der Faltwarte, Hähl, Hähl, Hähl, Hähl, Hähl, Hähl.
- `afriswitch/pidgin_03.wav`
  - Reference: Na the okal predo na e go call because like no people talk the bug stop satis stable So e must work round the drug to use enckure say make nobody cause am embarrassment and make nobody spoil him name
  - Actual: Na nio ka presidoo nai lego koi bikos Like oi bai wootok Di bok som sa ti stevu So im moz wok round the clock to use and show us a Menobody koi sa bai barasmet A menobody spoi ni ne
- `afriswitch/pidgin_04.wav`
  - Reference: Petroleum engineering petrol like petrol engineering why you leave petrol and come dey entertain us
  - Actual: Petroleum engineering. Petroleum engineering. Et why est-ce que tu l'as dit nos ?
- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual: Ah... Ok, le pro... Ok, le pro... Yeah, so... Beculho, so... E me ama a teoria desse vídeo, Anna.
- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: Păstogit pe cea pe cea urimeni ful, daz oa.
- `afriswitch/igbo_04.wav`
  - Reference: Look at the road network in Asaba ogba ogologo okpanam road make rain fall there
  - Actual: L'occasion de le dire, c'est l'art du coup qui m'a fait. Au bout de la mort, au bout de la mort. Je m'appelle Fordier.
- `clips/fintech_recorded/yo_01.wav`
  - Reference: Wo èyí tó kù nínú àkántì mi
  - Actual: 我以為都會弄我靠著命
- `clips/fintech_recorded/yo_02.wav`
  - Reference: Kí ni àkántì nómba?
  - Actual: Ki ni akant nomba mii.
- `clips/fintech_recorded/yo_03.wav`
  - Reference: Mo fẹ́ gba owó mi.
  - Actual: Música da Unii
- `clips/fintech_recorded/yo_04.wav`
  - Reference: Mo fẹ́ fi owó ránṣẹ́ sí…
  - Actual: Um desafio, ou não é que é si?
- `clips/fintech_recorded/yo_05.wav`
  - Reference: Àkántì nómba wo ló fẹ́ fi owó ránṣẹ́ sí?
  - Actual: Accounts n'ont pas ou l'offre-fi ou l'on chessie.
- `clips/fintech_recorded/yo_06.wav`
  - Reference: Báńkì wo ló fẹ́ fi owó ránṣẹ́ sí?
  - Actual: Banquiez-vous à l'OVERF et au moins chassis ?
- `clips/fintech_recorded/yo_07.wav`
  - Reference: Mo fẹ́ fi 500 naira ránṣẹ́ sí àkántì nómba wán yìí, 7011334637. Ṣé kì n tẹ̀ síwájú?
  - Actual: On fait 55 qui font de neura, la chessie a continuant bah on y, c'est un 11 des roues 1, 1, 2, 3, 3, 4, 6, 3, 7. J'ai qu'une tesywa du...
- `clips/fintech_recorded/yo_08.wav`
  - Reference: Ẹ̀san wo rè tí ṣe yọrí?
  - Actual: These are all ready to show you.
- `clips/fintech_recorded/ha_01.wav`
  - Reference: Ina so in cire kuɗi na
  - Actual: Ina să înțiliu cu inina.
- `clips/fintech_recorded/ha_02.wav`
  - Reference: tura kuɗin ya tafi cikin nasara
  - Actual: Tu locul in iata fi-ci gine-a salna.
- `clips/fintech_recorded/ha_03.wav`
  - Reference: Wani account numba za a tura
  - Actual: 1. Akaunt nombaza atura
- `clips/fintech_recorded/ha_04.wav`
  - Reference: Ina so in tura kuɗi ma .....
  - Actual: みなさん、トラクイーマー
- `clips/fintech_recorded/ha_05.wav`
  - Reference: Ina son in duba account balance ɗina
  - Actual: Hina Sun Duba akan balan stina.
- `clips/fintech_recorded/ha_06.wav`
  - Reference: Wace bank za a tura
  - Actual: Moci bancza a tuta
- `clips/fintech_recorded/ha_07.wav`
  - Reference: Lambar asusuna
  - Actual: L'embele à ce dessous-là.
- `clips/fintech_recorded/ha_08.wav`
  - Reference: Ina so in tura dari biyar(₦500) zuwa wannan account numba, dede ne?
  - Actual: Nasa turut dari biar Rizua Wanda Akan Nombah. Deden eh?
