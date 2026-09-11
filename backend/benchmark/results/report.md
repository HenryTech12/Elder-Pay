# STT Benchmark Report

Provider comparison on the clips listed in `clips/manifest.csv`.

## Macro-average WER / CER

| Language pair | sahara | groq | local_whisper |
| ha-en | 1.000 / 0.969 | 1.125 / 0.764 | 1.137 / 0.853 |
| ig-en | 0.619 / 0.299 | 0.499 / 0.308 | 1.121 / 0.610 |
| pcm-en | 0.357 / 0.246 | 0.433 / 0.271 | 0.637 / 0.423 |
| yo-en | 0.844 / 0.516 | 0.963 / 0.598 | 1.064 / 0.811 |

## Sahara queued-response fix

The previous benchmark accepted HTTP 200 responses marked `FILE_QUEUED` as final. The Sahara service now polls every non-`FILE_TRANSCRIBED` response, including queued HTTP 200 responses and the documented 503 response path, at no more than one status request every two seconds.

| Sahara benchmark | Successful clips | WER | CER |
| --- | ---: | ---: | ---: |
| Before queued-response fix | 20 | 0.705 | 0.508 |
| After queued-response fix | 20 | 0.705 | 0.508 |

The aggregate scores were unchanged on this 20-clip sample. The fix remains important because the old implementation could score an in-progress response as an empty transcript; this run confirms all 20 Sahara requests completed through the intended transcribed-result path.

## Intent exact-match accuracy

| Language pair | sahara | groq | local_whisper |
| ha-en | n/a | n/a | n/a |
| ig-en | n/a | n/a | n/a |
| pcm-en | n/a | n/a | n/a |
| yo-en | n/a | n/a | n/a |

## Observed failure modes

### sahara

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual: Kó ṣàámi náà, kọ́ sì gbà mí sí kan náà companies wọn so that mini ma ṣiṣẹ́ bẹ́ẹ̀ very shock pé ma fair assistly mapita

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
  - Actual: [empty transcript]

- `afriswitch/hausa_01.wav`
  - Reference: Saboda yanzu abinda ake yi ana daukan yanzu kamar iskan gas cikon mota ana Taliya dashi
  - Actual: [empty transcript]

- `afriswitch/hausa_02.wav`
  - Reference: Don dole haka na zama mai bada shawara saboda haka har guri ne da nima yanzu duk wani mai matsala zai zo ya same ni ga matsalata ko macen ko namiji to
  - Actual: Karin gwiwa shaida mana

- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual: [empty transcript]

- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual: Allah

- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual: Ọ kelekwere ọ kelekwere ọ kelesi remember we share this

- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: Pastọ ka ị kpechaa kpechaa, yor mee na full

### groq

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual:  Kondjo, kond shanwe, mi no, kond se igwa, mi se konno, kond pliz mo. So na ti, mi na li ma shishenwe, and I'm very shocked, but ma fei assist mi. John 3, o, don, re, mi. Ma apishete.
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual:  Meni, meni, meni.
- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual:  ੭ we. Can we do you say what we say . You may be given your money! Thank you very much! Thank you very much! Alright. Now, we had a lot of things to say, so let's start.
- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual:  Pisha qebo u losi investi kon lo, komo jen shi abosho loto, o deno onye adefe, o nye ode yo, o wolo de wala ye, lolo wala ye. Come on, ship that to your daughter.
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
  - Actual:  Puri bhūraṁ. Hakamāsavir mā tāpaśauraśa ya'kāri dhīrārātā nalā. Nāsak dhīra māyāsarāṁ na sātmā na kārāsarāṭa nalacayi yamalacayi. Tū.
- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual:  Perseverance, Resurrection, Affection, Love, and Pleasure. Affection, Love,
- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual:  Son of our action, watch out. Lose that to a considerable intruder. I can tell you so. I make you a character with incredible affection. Hello. I like to turn over a show. I'm a cautious luncheon
- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual:  oh
### local_whisper

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual: Quand tu a conchamé, mais non, quand c'est bon, c'est qu'on n'a pas complisement. Sur la dizaine, il m'allait m'achicher, mais à la vraie chôpe de ma fère, c'est ce que tu veux. Tu veux que tu veux, non, c'est vrai. Mais je vais te faire.
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual: Perna, vi non c'è mapei o con l'animi Ando ma voice in l'acestrogo di ormigli Oma voice di jabi non è Ovo voice? Poi non puoi giamo a voice? Eh? Si è toli po' di omo puri non lui si fai a pally?
- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual: 我告訴 you 我告訴 you 不錯 妳 妳在夢中 第二次妳 妳 妳設計妳 妳 那妳左邊
- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual: 視聴者のダメである museuではありれば variantsっている ということを実施することにも欄に伴っていく 同様に発生するのは現ément 幸福を Celebrいたメロディーンで 歩き 話は言われててず それは歌詞や 反県関する 与え生る という皆さんが 中国が
- `afriswitch/yoruba_04.wav`
  - Reference: Mi ko ma ran, ko ma ma mu oriburuku ko mi mu, lọ funrarẹ, Abi ki o ri gun, kii foriburuku yé na? ti mo bímọ tán kín ṣẹ ma wa ọmọ ti ma rent ko lọ bámi ra ọja wa? Ẹ̀bi rẹ kó. ṣe wọ lo lọmọ ni? ẹ sẹbi rẹ ṣẹ.
  - Actual: Mey, Kamala, Kamala, Kamala, Mahmoudi, Pruku, Kamemo, Lafurale, Abkhirani, Kamekir Puri, Puku, Yena. Ezimobi, Madhaktin, Zehmao, Mahmoudi, Mahrenti, Kola, Mahmoudi, Dawa. Tevalo, Laman. Eh, Shabirase. Ah!
- `afriswitch/hausa_00.wav`
  - Reference: Ya ce haraje haraje na Amurka a kan tarayya Turai za su kara rura wutar kalubalen da nahiyar tiri ke fama da su a cewarsa yakin kasuwancin da donald trump ya kaddamar
  - Actual: Hi. Hi. Hello. Hi. hi. Hi. Hi. Hi. Hi. Hey. Hi. So... Hi. Hi. Hi. Hi. How are you? How are you? how is your belly? Hey. Hey. Hi. Hello. Hi. Nice to meet you all. No, I'm sure that
- `afriswitch/hausa_01.wav`
  - Reference: Saboda yanzu abinda ake yi ana daukan yanzu kamar iskan gas cikon mota ana Taliya dashi
  - Actual: Shit my 재미 I thought I'd just Fuck off Got to come Don't stop Dead our Shit my speech
- `afriswitch/hausa_02.wav`
  - Reference: Don dole haka na zama mai bada shawara saboda haka har guri ne da nima yanzu duk wani mai matsala zai zo ya same ni ga matsalata ko macen ko namiji to
  - Actual: colour 내려哭 assa passé cond hour day ill ahahahahahahahahahah j Properse wizard e Resworth level ebe ye
- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual: [empty transcript]
- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual: Schöner auf Wackfahr Lücher zeredrchen, Ich hatte das in den Fümmel Acktelecher Ich hatte das in den Fümmel Ich hatte das in den Fümmel Für die Fümmel Verlattes Schöner Hähl, Hähl, Hähl, Hähl, Hähl, Hähl.
- `afriswitch/pidgin_04.wav`
  - Reference: Petroleum engineering petrol like petrol engineering why you leave petrol and come dey entertain us
  - Actual: Petroleum engineering. Petroleum engineering. Et why est-ce que tu l'as dit nos ?
- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual: Ah! Ok, leionou, ok leionou, ok leionou, ok leionou, ok leionou, ok leionou, ok leionou, ok leionou... Isso é uma matricia de esse vídeo, ah!
- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: Păstogit pe cea pe cea urimeni ful, daz oa.
- `afriswitch/igbo_04.wav`
  - Reference: Look at the road network in Asaba ogba ogologo okpanam road make rain fall there
  - Actual: Le cartes du goût de networking a sa main. Où går le roe? Opera un roeut et un goût japoncil.
