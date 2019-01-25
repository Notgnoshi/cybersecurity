#!/usr/bin/env python3
from string import ascii_uppercase

ALPHABET = frozenset(ascii_uppercase + ' ')

plaintext = """Having obtained an audience of the King an Ingenious Patriot pulled a paper from his pocket, saying:

“May it please your Majesty, I have here a formula for constructing armour-plating which no gun can pierce.  If these plates are adopted in the Royal Navy our warships will be invulnerable, and therefore invincible.  Here, also, are reports of your Majesty’s Ministers, attesting the value of the invention.  I will part with my right in it for a million tumtums.”

After examining the papers, the King put them away and promised him an order on the Lord High Treasurer of the Extortion Department for a million tumtums.

“And here,” said the Ingenious Patriot, pulling another paper from another pocket, “are the working plans of a gun that I have invented, which will pierce that armour.  Your Majesty’s Royal Brother, the Emperor of Bang, is anxious to purchase it, but loyalty to your Majesty’s throne and person constrains me to offer it first to your Majesty.  The price is one million tumtums.”

Having received the promise of another check, he thrust his hand into still another pocket, remarking:

“The price of the irresistible gun would have been much greater, your Majesty, but for the fact that its missiles can be so effectively averted by my peculiar method of treating the armour plates with a new—”

The King signed to the Great Head Factotum to approach.

“Search this man,” he said, “and report how many pockets he has.”

“Forty-three, Sire,” said the Great Head Factotum, completing the scrutiny.

“May it please your Majesty,” cried the Ingenious Patriot, in terror, “one of them contains tobacco.”

“Hold him up by the ankles and shake him,” said the King; “then give him a check for forty-two million tumtums and put him to death.  Let a decree issue declaring ingenuity a capital offence.”

“Your Honour,” said an Attorney, rising, “what is the present status of this case—as far as it has gone?”

“I have given a judgment for the residuary legatee under the will,” said the Court, “put the costs upon the contestants, decided all questions relating to fees and other charges; and, in short, the estate in litigation has been settled, with all controversies, disputes, misunderstandings, and differences of opinion thereunto appertaining.”

“Ah, yes, I see,” said the Attorney, thoughtfully, “we are making progress—we are getting on famously.”

“Progress?” echoed the Judge—“progress?  Why, sir, the matter is concluded!”

“Exactly, exactly; it had to be concluded in order to give relevancy to the motion that I am about to make.  Your Honour, I move that the judgment of the Court be set aside and the case reopened.”

“Upon what ground, sir?” the Judge asked in surprise.

“Upon the ground,” said the Attorney, “that after paying all fees and expenses of litigation and all charges against the estate there will still be something left.”

“There may have been an error,” said His Honour, thoughtfully—“the Court may have underestimated the value of the estate.  The motion is taken under advisement.”"""

plaintext = ''.join(filter(ALPHABET.__contains__, plaintext.upper()))
print(plaintext)
print('words:', len(plaintext.split()))
print('='*80)

plaintext = ''.join(filter(frozenset(ascii_uppercase).__contains__, plaintext))
print(plaintext)

key="ambrose"
ciphertext = """HMWZBYSBFBZBWHAZBLRAINOFFTLLEWJEUSRIZHVBASUEQRHJMOFQLZDIDMQRDWVFDPDVAWPADBSLWAKJEUEEYUUGZWESQZFIJQAVFJHQMHMWVVWVEMGFFEYLMGFFUSNEUIIUXIZHRFESUDQCOLMNSXYWULNAHLBUENBJVFUIIRUYSKIPXBKSKERQBUCHXEPJEHZIRAZRZFEVKPLFOEREIZDKAIXMSSARVGMESJEBXFRBVXHQSVTGVEUOMWFGINMVVWVEMMJCSVEDFGCJXSAGPCMVMMKVGLCSYJEWKXEDTRHLISFJEULLEHBCIWSFFIVWFZEZUZCFMWUMCDSVTIJKVECRUHYHARIFGFFSQIXMZCFXUYULAKEFFFISPEMUOZBYXHQQRDWVSFIVYARGBVKHZIMMXRMSRDBSFAAWEPIZASRODEVFGRTTFCCJHHUHYHJIAEVISJSFFIVSPXODUZCFHEBBIHEINFGFFSQIXMZCFXUYULAKENPIVFWWAUEKVWMNSFEWGYSBBKFASTBVCZARGMOFHZIRBBGSJJRANRBGXHQSGCUOEFBISLLEIPIYARGBMRBKSFMHLBLLAFJYONIIZWVBLIDIIZQZAIXMGWWVCQUYOLERYPLFQSUDNRXWWTKTICQELNSFHZIRFIVSETEDPICXFAZHZGSRXUPLGLSPGSTVSWEUUSILPOKBCHQXOKPLFEEJQTKMKXHDPESSRDBFIGGRCAOJHJEIZTDSLSORGVFAXFUSJHLSYAVIASNEEUPHZIPDJTSAWOZFDWDPIAOKIEXUYTYONMNSSVQWMVQEKVWTRANZGWSFMOFHZIROIVQCLEFIIIKXHUTYOFHIZUFGLMLXBECLLEDQFQCITDFDOJOIZHKVWTRUDVCXXHQJIFWWIEUZPDIGGONCMPDTBMSTIEZNLQZKRQBKSJCOGSDOBISFZSILJODUYSXECFUYOLMTENZGKMLQTTOFFEEPVTXICFJMSDCAHFIHWHBKNPDWGUXJRFEITTPUCXXRQBKWFKTTFRFESUDQCOLISIJKVSREIUYSCMNSTZUFIDFPKVWKRQBKVWEDRBTHGXUYUFOHTRABTVKIADDYHZMSYBEVWWAUERBVVEBPIHZSWYBEMHSCWFKGZIHMTWCJXYFIISWWIDFJOAHTTFXFWETTFRRXECFPKIEGOYQCSLMNSUYSKGRGUZBQQAKJKDDIAEFPCMVMMKVGLCCDJVRLLEUOXSFMOGTGOLVIAUZBLIRDPICFIORUYSEGOZURWFWTACRQUSHAMUVAQUBCPHZIAZLCSKENPTYOCIHUNJOAHTTFBWFKTTFEUAZETJDOULEOLWCJJODUPHOSMUMCWGRTGNKIEWAZEGILLIYUFRWETTMVHSHEOSVSAWSGFUSUPADJEUARGQOLWLCAOBGWLELAGWSFGEKPLFZSNAVIGSMDMORHLSRZFPFAWIZHNVSXIEUYSHVEEFEHKXAFVJCXXHUTTOKIAEGRFSWIFIRGYSNQJYONIGUWVBSNUPHDSFXFASKVWVEEJUISVYXFXOLIEGOUSJXHQXZZDWAUEKVWGOGSKDMXTTFTCKXSGQFBLLEOPEHWWTMOKGVICUEVRSPLCVVGLMOZTISDETUOXHGJEQTRBVSTTFIQZERSFJOFHIZTYCJXTTFVGLETQJEZAXISBKWGRHMTSSWRSQUKZWHWUUYODPCAOKFGZEDTZSKHIEQLHWWMUTLBVIREURBVMNSTRBVHIRGVFWRCQTFTGTIZJFBLLEDFLBLSABQVFLEIZJEUSLYQTZGWISMJUHZIAFUFFFIYFIFIYLTRVCZQAEMSVASOIZHGFGKRQTJKWERQHVHLMNSPETSQOGTCMHVOSSVGKICTPVRLLEVVUUWTRAHISKWWTZJWJXHQNRHLIRUTTCFGLGEVRWBAOUCMWBAOUCMAXHMEKCTICAOTZMHEPJECJHEDUFUAZEDFCSNENOZKCLLEYPKWGRTTBKWSQANPLHLSMMLVMGYRTPECMVIYPMSLLAFUYSBYDSNVBLSFFIVQGYRFCVGWXAEJUSSRDFIVQSWEDFFDWREPVGCFAHMUXFGYNPTZFLLEVVUUWESWFUWFWUDQIWKIUBPEHZIGDPLBVWAUEKVWETFPIBWCTTBKOXXEDQRMARGMMCTWISMOUSPTEZTVGGJLUUZUSXIAORBVELXDYOJKEEBXOARSFUYSWWTMUVHZIRQXZZDWTUMCPWWOYFKVARGXFWHLLEDFDOQLAHFSSWRAZFIFGVSMJUVAWHAOFIJXHAVXVLJUXMPHZICAVIHEEYTBMSMRDQSVGLMMMUVRLLEHBCIWSFFIVSKXAFFKVWQOFJFBAWTMLVBMRDQSRRNMSQNVBL"""
