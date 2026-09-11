# STT Benchmark Report

Provider comparison on the clips listed in `clips/manifest.csv`.

## Macro-average WER / CER

| Language pair | sahara | groq | local_whisper |
| ha-en | 1.000 / 0.969 | 1.125 / 0.746 | 1.325 / 1.031 |
| ig-en | 0.619 / 0.299 | 0.644 / 0.478 | 1.009 / 0.548 |
| pcm-en | 0.357 / 0.246 | 0.443 / 0.290 | 0.667 / 0.446 |
| yo-en | 0.844 / 0.516 | 1.045 / 0.583 | 1.098 / 0.800 |

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

## Groq domain-prompt ablation

The production Groq path keeps its banking vocabulary prompt enabled by default. This benchmark disables that prompt so the out-of-domain AfriSwitch clips measure transcription ability without banking-vocabulary bias.

| Groq configuration | Successful clips | WER | CER |
| --- | ---: | ---: | ---: |
| Prompt enabled (prior run) | 20 | 0.848 | 0.607 |
| Prompt disabled (current run) | 20 | 0.814 | 0.524 |

Removing the prompt improved Groq by 0.033 WER and 0.083 CER on this 20-clip sample. The change was meaningful, but not dramatic; the prompt was not the sole cause of the high error rates. It also removed the earlier `ig`/`pcm` request failures because unsupported language hints now use Groq auto-detection.

- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: Pastọ ka ị kpechaa kpechaa, yor mee na full

### groq

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual:  kon jo kon shanwe mi nyo, kon se ikwa mi se kon nyo on komple ti zi nyo. So, dati, mi nali ma shi shenbe, and I'm very shocked but ma fei asistni. John Trio, Lauren. Ma apishi te.
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual:  On my boy, she was angry with me. And on my boy's end, I have a struggle. On my boy's, he had a big fight. My boy, she was angry with my boy. She was angry to see my son
- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual:  Thank you so much Let's do it, guys Ok, let's do it Ah Now, let's start with the shell Time is up
- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual:  Pisha Chibu lòs investi kon lòk wò mò chen ʷi à bò tion lò tò. O ndenon, nye à dè fè, o nden yò, o wò lò dè wà lá yè, lò wà lá yè. Come on, ship that to your daughter.
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
  - Actual:  Puri Pura Hukam nasa yon agata sa yon aapari yon arahata na lo ya zakti yon amayas amayas masah na amayas amayas amayas yon lechay yon lechay Ki
- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual:  Pesakar ayam shukrishakum. Sambil matrim hirangan matrim. Matrim matrim shukrishakum.
- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual:  Son of our action, watch out. Lose that to a considerable intruder. I can tell you so. I make you a character with incredible affection. Hello. I like to turn over a show. I'm a cautious luncheon
- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual:  oh
- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: [empty transcript]
### local_whisper

- `afriswitch/yoruba_00.wav`
  - Reference: kọn jọ kọn ṣaanu emi naa kọn tiẹ gba mi si ikan ninu awọn companies wọn so that emi naa a le maa ṣiṣẹ nbẹ and am very sure pe o ma fẹ assist mi jọọ ntori Ọlọrun o ṣẹ dear
  - Actual: Quand tu a conchamé, mais non, quand c'est bon, c'est qu'on n'a pas complisement. Sur la dizaine, il m'allait m'achicher, mais à la vraie chôpe de ma fère, c'est ce que tu veux. Tu veux que tu veux, non, c'est vrai. Mais je vais te faire.
- `afriswitch/yoruba_01.wav`
  - Reference: E ma binu. Se e mo pe okunrin ni mi and omo boys ni lati struggle lo. Omo boys jagun lo ni Omo boys? Tori pe o je omo boys? Se tori pe o je omo okunrin na lo se fe pa mi?
  - Actual: Perna, vi non c'è mapei o con l'animi Ando ma voice in l'acestrogo di ormigli Oma voice di jabi non è Ovo voice? Poi non puoi giamo a voice? Eh? Si è toli po' di omo puri non lui si fai a pally?
- `afriswitch/yoruba_02.wav`
  - Reference: to ba je nkan to ma wu e to ma mu nu e dun niyen anyway mo agree pelu e ah ah, ese oko mi thank you so much se iwo nan ti gboun e bayen, ori mi gidigidi gan ni ah ehm nkan to ma sele nisin nipe taba ma fi ri
  - Actual: Ben, storybook, Toma, I'm going to my moon right, don't you hear? I don't hear. I'm going to my moon right. Ah, sure. Ah, sure. And she'll call me. Thank you so much. That's why I'm not a boom, eh? All right, let me get you a gun, eh? Eh, now, I got your martial arts in AP. Toma, my theory.
- `afriswitch/yoruba_03.wav`
  - Reference: Kisape olosi university oloko banse sabortion loto ode nani ade fe oyun ode yo iwo lóde walaye owa laye, common shift that to your daughter
  - Actual: 私は活用する場所です。 私が必要となり、私は協力がありません。
- `afriswitch/yoruba_04.wav`
  - Reference: Mi ko ma ran, ko ma ma mu oriburuku ko mi mu, lọ funrarẹ, Abi ki o ri gun, kii foriburuku yé na? ti mo bímọ tán kín ṣẹ ma wa ọmọ ti ma rent ko lọ bámi ra ọja wa? Ẹ̀bi rẹ kó. ṣe wọ lo lọmọ ni? ẹ sẹbi rẹ ṣẹ.
  - Actual: Mey, Kamala, Kamala, Kamala, Mahmoudi, Pruku, Kamemo, Lafurale, Abkhirani, Kamekir Puri, Puku, Yena. Ezimobi, Madhaktin, Zehmao, Mahmoudi, Mahrenti, Kola, Mahmoudi, Dawa. Tevalo, Laman. Eh, Shabirase. Ah!
- `afriswitch/hausa_00.wav`
  - Reference: Ya ce haraje haraje na Amurka a kan tarayya Turai za su kara rura wutar kalubalen da nahiyar tiri ke fama da su a cewarsa yakin kasuwancin da donald trump ya kaddamar
  - Actual: Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, Anse, An
- `afriswitch/hausa_01.wav`
  - Reference: Saboda yanzu abinda ake yi ana daukan yanzu kamar iskan gas cikon mota ana Taliya dashi
  - Actual: Chme tra Revol까 Fife Consult Sa schnell Non strappani Knomp Chme tra Revol까
- `afriswitch/hausa_02.wav`
  - Reference: Don dole haka na zama mai bada shawara saboda haka har guri ne da nima yanzu duk wani mai matsala zai zo ya same ni ga matsalata ko macen ko namiji to
  - Actual: tan Awwrrrrrrr rha rha rha rama rha rha rha rha rha rha rha rha se rha rha adjustment la raha da larsasha, rha rha rha s Doo pur s rins ma bham meta rha rha r included mistake y aldh 가� ting?
- `afriswitch/hausa_03.wav`
  - Reference: Maka ga gawan shi ma saduda amma ace kwana da kwanaki mutu a rasa inda yake
  - Actual: [empty transcript]
- `afriswitch/hausa_04.wav`
  - Reference: Sanya ganyayyaki, wake, man zaitun a cikin tsarin abincin mutum yakan kawo sauki da kuma taimakawa wajen kara lafiyar jiki. Har ila yau, yawaita cin naman shanu yana kara zafin wannan ciwo.
  - Actual: Schaner auf, wir klar, wir schaht zurück, anscheide an den Füllte, akentelische Karte, wir taugelt für wir von anderen, für alle, Verlarte, Ich habe es nicht mehr. Ich habe es nicht mehr.
- `afriswitch/pidgin_03.wav`
  - Reference: Na the okal predo na e go call because like no people talk the bug stop satis stable So e must work round the drug to use enckure say make nobody cause am embarrassment and make nobody spoil him name
  - Actual: Na niok apresidoo, na ilego copikos, na koimai wo utok ni bok som sa tis tebu So im moz wok round the clock to use and show us a minobody cos a min barassment a minobody spoi ni neop
- `afriswitch/pidgin_04.wav`
  - Reference: Petroleum engineering petrol like petrol engineering why you leave petrol and come dey entertain us
  - Actual: Petroleum engineering. Petroleum engineering. Et why est-ce que tu l'as dit nos ?
- `afriswitch/igbo_00.wav`
  - Reference: Awwwwn okelekwere okelekwere okelekwere, biko remember to share this video and.. yes o
  - Actual: Ah... Ok, le pro... Eu sou... Porque eu me ama uma chica de esse vídeo, Anna.
- `afriswitch/igbo_01.wav`
  - Reference: Pastor gị kpechaa kpechaa, you remain a fool. That's why
  - Actual: Păstogit pe cea pe cea urimeni ful, daz oa.
- `afriswitch/igbo_04.wav`
  - Reference: Look at the road network in Asaba ogba ogologo okpanam road make rain fall there
  - Actual: Lucas du code netwalkée n'a jamais. A ou à quoi que le code ? A ou à la route ? Ma crises forgakt.
