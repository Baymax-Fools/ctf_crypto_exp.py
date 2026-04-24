import string
import itertools
from Crypto.Util.number import *

s = 'vev4uuuuvyv42eove2f81mmvouuvo1mmvyuuvd5v333434333436353533343433f1jvsds320b1b91e2yquuuuveve3xyuu2eo2eov560bf34343335353733333335bh348o8n5v5w8n8o5v335v335x5vbf5v5x33338s5we95y5v3434335v8n5w33345v3433338n5v5v333336368rbf5v34335w353334345v8r345v3434373333355v3434365v33335w3361345z5v33338n5v5v33bh3533ec3333bf8n355x338n335w33bf335v343633h0365w3633335v338n8t3433bf5x8n5w338n3533345v35338q5v33bsns3sd1jv1kps333fs31jvs32bn2c7s31k53vh1jv2bns32bnsd1kfs3s31kf4mzs31jvsds3sx1jv1k5sx3v7sn1jv1kf33f1kpsnsdsn1jv1jv1jv2bnsxs3sd1kfths32bx2bn2bxsx1k51jv349s31jv1jv1jv3vh1kf1k5s333p1kzub2bn5fl2c7sd1k5s32c71k51k5sn2cht7sns31k51jvsn1kp1kp1kpt7t7sn2bxs3t72bx1jv1kfs4uoun1bc12yxe12yxe18jxdumxdxe1e2ulxf12xul10618huo12xulxgxixduluo12y108xdulumumxdumun105um105um15p1b9xexdunulumul12x10610512yxe12yul105up106ulxdunuluo12zusxlumun15r12yumulul15ruqutuluo15qxexfulxhxgul106ul105umum12yxe131xd15qunum15putumululuoulxf12yxkul15qul12zulul107xd1e3xdumulum18hulum10512y10512y12yxf108umuqxfxguq107xgxexd1bcxium106ulxdxe10512y105ulxe15pxjxgum12xxh12xxi105umxhxdunxdul105umulup105ulul106ul105umum12yxe106un10512yul130105xexdumuq12x32uu1o0w8uu36qvo1mw1ngvouux2uuv4uuv42ey366veuuuuv4v437u1n61mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuw8uuve1mm1mwuu1mm1ng1mw1ngvouuuuvy3701n61mw3yivo1mw1ng1n6uuv4vouu36636guu2gc69a3xyuuuuuu1mmw81nq1mm2ee3xyv43yiuuv41nqv41nqvev41ok1mm5w335w333535333333348n333333345w5v5y338o8n3433343436jr5v33bf345v338o5vgz333435333433358n333333333334338o8o33348o33338p5w33348n335w5v5z8r335w3733e9jr8n5v33335v5v8p33mj8n355z338p5v333333335v355y333334mj8o33338n5ybg8n8n5w353333h033335w34335w5xbfbf33355z3334338nbhgz335v33mk33bh338p34345v34335w395w35355v5vgz34e83535388p348obhbf33335x373434bh5v5v34345w335x358p338n8n333334333333355xbg5v348n8p8o36348o348o345v33e83533345w383435333336335y335y5v338n355v3333335w5x5ve739338n5v8n33343333345x37bf335v3534e78n33bie9336233jr8o8n5v335x34338o333334335v5x5v5w33333633368p5v5w34375x3533h4335w5v5v345vbg5w8n33335w3333345w33335v37338o33343a8o345x5v355vh15v8n5v628o3435375v33bf33343335338n345v5x5v3336335xbg5vjr37355x5v8obf8n348o3433345w8n35335v33345vsd1kps3sds3sds3sd2bnsd5f11l91k52bxs32bn1jv2ch1jvsd2bnsd1jvt72c7sds3snsds31jvsxsn33fsdt7s3s3sd33fsdsxsx2bx1jvsn2ch2chs3snth1k51jvs3s3sn2bn2cr1jv4n933psns3sdsns3sxsdsd1jv1jvsdsd3492bxsd3wbsx2bnsd4n9sdsns3sd1k51jvsd1k51k533psds31kf33zsnsd1jv1kzsd5er1kzs3s31kfs31kf3w1sns333z4mzs3sdsnsd1jvs32bxs3sxs3s31jvs32bnsx2bxsd2chs3s3s32bnth1k533fsns32bxsx1jv1kfsd1kps3sdsx1k52bx1k5sn1kfs3s31jvs3sd1jvsd1jv2chsn1jvsds3t71kz1jvs32bxs3sx2ch3vr2bnt71jvsx33f1k53vr1jvs32bn2bn2c72chsxsdsn1jv2bns3s31jvsd1k51kf1k5sd1jvs3s3sxthsdsdsdsns31lj349snt7sns32bnsd1jvs3s3s31jv1jv34jsdsd1jvsdt71kfs3sd1jv2bnsn1jv2bn673s31jvs3s3s333f2cr3v7sd1jvsd3vhs32bx1kfsxsnt71jvsn4mz2bnsdsns3s32c72bxs3s3sdsds3sd1jvs31jvsdsd1kp2bn1kfsdsxt72c71k51kps31kp2bx1jv3493vh2ch33zsx2bxs3ths3sd1jv1jvs32bxs31kf1k51jv1jv1k5sn1jvsds31k5s32bns3s32bxsds31kfs3s3sn33p1k52bn1k5349sn2bx1jvs3s333psns3s31jvsx1jvs3sds32bxs33v71kfs333f33z1jv1kpsxsxs33v71jvs3sn1kf1jv33f1jvsnsdsx1jvsd1k52d1s3sdsns31k5s31jv33ft7sds333fsn2bn2c71jvsdsnsx1k5s31k52bxsd33psds3s3s31kps333ps31k533f349snsds31k5sd2bnsd1jvs3s3s31jv1kfsn33p1jv1kps3sns3s32bxsxsn1jv1jvsd33ps3s3s3s31kp1jvs32bxs333ps3s33vh1kps333p2bns31kf1jvsn1jvs31kp1jvsdsdsns3s32bns3sd1jv1k51jv33ft71k5sdsdsd2c7s32bx2bxsnsd2bns32bxsnsx33ps31kf33fsds32bxs3sd1jv1jv2bxs3s3s3snsd2bns3sxs34nt1kpsdsds32bx1jvsn1jv33p1k5s32chs31kf33fsn2bx1k5sns3sns31kf33fs31jv1k5snsn2c7rtxdunum106um12xumxe15q107upulxeumul2fi3661mm384vyuuuu4qk2eev41mm1mm1n61mm2f8vo1mmve1ng366uu71wv4v41mm1mwvev4uu1n61n62eo2eeuu1mm5hi2eo1ng2ee1mm1mm2eev45hsuu2ee4q036q1mmvyuu2ee1nquuuuuuvo36g2eeuuveuu1mwve2f82eev43xy1mmuuvev4uuuu36guu36quuv41mmuuvewiuuv43701mmuu366veuu3ys2eeuu6aouuve1mmv4wi2ee1n6370uu2eo1mmuu2eew8uuuuv4366vouu2eeuu3y81mm1o02ee2eeuu2ee1nguu1mmuuuuuuv4v41mwv4v4uuvo366uu2eyv43xyuu69avevo2eeuu3xy1mmuuuuuu36q1n62ey36g2eo1mm2ey1mm1mwuuvev4v45hive1mmv41ng37u2f8v41mw2eew8v4v41n61mmv43xyuu1mm1mwve3xy2eovo4qa2eyuuuuuuuuuuv4uuuu1mmuu2eov4uu1mm2eyv4uu1mmv45i21mwuuuuve1ng1ng1mm1mwuuvovo1mmuuvy1mm1mmuu2ee1nguu1n6v4uu2eev41mm2eo2eouuv4uuuuv4s58n33e85v33gz33h05w5v3833378o3333345w34bie95v33333733bf5w36333533358o8o8o5v8o33bgbf3336345w335v36gz33348o3338338n33338p34353333338n33358o5w335v3335bfe9bh5w365v3435e73335e7335x358n5vbf5w33345w5w338n5v8n3334345xbf5w3833ebbf5x8p8o35345x5v36bg34333533348n5v335v33gz8n5w33bf8n35348s335x33343533333336343533h0338p345xbf3633333334338p5v33335v3433333437bf33345wh25v348o5we860333533bh5v3334bi33335v3334bg5ve75wec33368n33355v5w5v8ph13333618n3333338n5x5v35338n33bf338n33365v335v34gz3334335v335x335w3433335y3333333433bf33378pe7335w5v348ne8bfe78n8n33bj34bh345we833335v3533333437bf35ec345ve733333339bh37eb5wbf345w3338338p345w335v355v8o33335v5x8n638n5v5v8n5z335v338qbg335z333334355y5w335w33338o33335v3335345w33343334335ve95v5v5v34335w5v35e833348n345v5v33385x5w8o8q5v35e73433e95v5y3433338o34335v335v8o8n5v5xbf338o33335x35338n333333375v5w33335v335w348o8n33e7358o5wbf33333436bf5v348n5w5x5v8o5w37345x35bf8n33343534605v33338n34335v3333jr8n5v33333333348n5x5v5v348n3534338o33333335335v8n355w348q35bf5w33605v345v33jr8n5w33bf34ju8n5v33e7ju8o5x34bf8p603333338qe7bf8npdgz335v338n5v3334gz8n368n335v5v345x333333358n5y8n33bg34365v36bfpb5w5w5v8n5v5x343333bf335v5v8qe7bf5vbf5v335we7368obf348n343333335w343335353334388o33338n345ve78p34335ze8338n37bg335w348o373333363434343334bh3334e8bhbg33bf5y35gzbf8p3334345v34bf335v8o3334368n8o335vbf8p5v348n8n335v34335v5v338re8jr335y345x37e733bg348n33bk5y375w8n33355w5w33343734345v5vbf3338345w36gze733358n335x5y35335y335v345v338p33353333bf3333bg5y33338n5v8n8n375y5x5v5w375v345w5vbf5v335v3333338oe75v355x345w5v345w3434e85v8n5x34338n33345v5v5v8sbf5w35333533e734345y3333bf8n34365v33bf358n5v5vbh5x358n338n3335jr5v5v8qbf368nbf5w8o5w35335w338o345y33335v5w335w335v348p5v5v34343336e98n338n8o358o5x3433jr5v5w385w333333h03334333433bie734338o33365v355v33355w5v335w8p5v5w33335x5we85v33bf5v5v8o5w8n33338o365x33355v355x35345y375v348p5v5x8rbf348o8p335vjr5v33333333335w5wjr6236345v5v5w5w358n33348n5v8n5z3436333637mj5w335v338obf6033335v8o335xbf343734343433368oe95w338p3434bgbg338oe75v5w5v3533335v3334345x8n355xbf8n335v333335bgbj5v8n365w335ze78q5x8n5w338n33338p363434345ye7333433345v3433343333338pbf8n8qe7353433bje733333436338n355v36e85v8p8n33bf33bf335v355w5w3333338n5w365w5wgz3336bf5y33355v5w34345v358n33358r363533h1bf335x5v348n335w5w5xbf8n34345v3333335xbf8nbf385v33338nh03335338n5v8n8n5y8n338n8n33335y3333e98o3336378p8o5v33e75vbg3333375v5v5w335w335v36355v8n345xbi8o5v358obf3533345wbf3433378o5v8q335w5w5x5v5w335ve78o34345y385wbf365v5x5w5v358n34ea333435338nbf5wbf3534bf5x5w8p5v5x8o345vbf365v345w8obf37ea8n8o335y34395v5w5v3333365xbf355w33335x335v5ybf33bf348t34343333338q8ne7355x34jw5v5w36365v34338n338n335v5v36e8338n8o338o335v333833bijs335v3333345v345z8nbgmj8p33335x3435355v3533335v5w338n5w33335v8n35345v333d33fs3s31kfsx2bn3vh1k5sd3v72bn1kp1kf1k51kf1jvs3s3sdsd1kz2bnsn33fs31k52crsd33psdsn2bnsd1jvsd1k5s32bxsdsnsds3snsd2bxt7s31jv33psdsn1jvsdsdsx2bn2bns31kfs31k51jv3v71jv1kzs32bn33psxs31k51jvs31jv2bn33f3v73w1sds33v7sd1kf1kf1k51jvs31jvsd2ch1k51jv1jv1jv1kf2bxs3sdsnsxs31kf1jvsns333f1k5s31kf1jv2bnsdsns3sx1jv1k5s31kps3s333f1k53491jvsx2c7s3349s32chs3sd1lj1kf1k5sds31jv1jv2bn1kfsxsd1kzs3sns32bn2c733p1jvt72bns32bxsn1k5s31jvsd2bns33vh1kp1k52bn2bnt7sn1jv1k5snsd1k51jv2bxsn2bx1jvs32c71k5s32bx1k52chs31jv2c7s3t71k51jvs3sns334t2bns3sn3492bn2bn3vrs3sn1kf1kp1jvs3s31jvsx2bn1jvs32bns31k51jv2bn4mz1k5s3s3t73vh1k51k5s31kfs3s34o3sns3s334933zsnt71kf1kps3s31kf2bnt72bns31k5s3sd1jv1jvsn1jv1k5sxs3s3s3t733psdsn33f5ers34ntsxsd4mzs32bn1k5sds3s3105ululunxeul18i12yumulxdumxexg106ul15qululumunul107uo12zul131un105umxdumxeul106um105108xdumunxeul106106105ululumxgulul105xeumulunxe130up105ul105uoumvo36q36guu1n6uuvo1mwuu2ee1mmv4uuuu1mw2ee1n6veuu3yi2ey1mm4qa1n6ve1mwuu1mw1mwvev43661mw366vove1nq3xy1mm1mm1mm3xyuu2ee1okv41mmvev41n6vy2ee1nguuuuv43xy1mmuuuu2ey2eev41mwv42eo1n6ve1mwveve1mmuuve2eev4uuuu2eo2f83661nquuuu4pqv42eo1n62eo2ee1mw1ngws2ey366uuvo1mmuuuu2eeuuuu1mm1mw2eo1mmuuuu1mm1ng1mmw81ng2ee4pq5i2uuvo1mmvy3y8vy3xyve1mm1mw1ok36q1mw1nq1mmuu3662eeuuuuuuve1mm3xy1mw2eeuuve1mm2ey1mw2eeuuv4v41nq2eouuv4uu1mm1mm2eov4366uu2five2ee1mwuuvo71236g2eevo2f83663663xyv4uuuu36g1ngv4uu4q01mm3661n61mm1mmv4vy2ey1mm2eouuv4370366uu1n62eev41n6v44pq2eo2eeve2eev4vo2eev4uu1mmuu3ys3y81mwv41nguu36gv4v4v4v41n61mm3xyuuv41n6uuv4vouuv4uu3662eeuuv4vyuu37auuv41mmv4v41mm2ey1mw3z2v4veuuvo1mm1mw1mm1mm3xy1mm2ee1mmws36qv42eeuuwive37ave2ey1mwv4uu36g2ee1mwuuvo2eo1mmuuv436guuv4w81n6v4uu2eevo36q1mmuuuu1mm2ee1mm1mm2eev43xy1mm1mmw81mwuuuuve1mm3xyv41o0uuuu1mwuuvev4v4uu3702eevy3701mm1mw4res68o5v33358r8n3333335x5z5v5y5v338nbfh035bf335v5w333333bk8oe7338p8s333433bh34338n5w335v333433355v3633335w5v338n8n8r618n338n8o348o335w33338n333634345w335x33333a36gz3333bg35343336335v348o8o3335368n343539bf5x5v33bf8n5z8pbi348nbg5v5w35bf335v8n8t8o8n333533348p333534338p338p33348obgh233355w8o5v33638n5vh0js34343533e8bh345w338s3333395v5ye7e7e75v343a338p34335w35335wbf335v3334345vbh8n3435345x33bf335v8n37bf5x34335z33343a3333335v8o5w5v335y3536335v8n33343333bf5wbh5v5v335v8n37335v33335w5v5w33365v5v335v5v8o5v33345w363435343334368n338n345v8q365w38345v8q343334bgbf33358q3334335w335v34335xh15w3660bf5v35gz335w8n333434343333335v335w8n338o345v38335v5x5w335v333634333334345w8n355v5x335w8n5z338n5vbg343435358n8o3536345w345w355we88p5v333333343536335v8p335w335w34333433355vjr34333437355y33348o5w34335v33bf33345w5w33e75v8q37338s5w5w335w8o8n5v3534bf333835bg3433bk35335v34bg34bf33338o5w5v3433338p2t4mzs3s3s32bxsd1jv1jvs3s3s31jvs3sdsdsxs3sd1jv1jvs31k5sd1kfsd1k5s31kz2bn2c71jvs3sd2bns3s3s31k5s3s31k51jvs3s31jv3vhs32c7s32bx1jv1k533ps3s3sn3vr1k5s31jv3v71jv1k5s31k52bn1k51jvsnrvumxd12x12x12xun106xduoul131ulxd106xdxdulxeul106umxgxf107ul15qulxdxdvo2ee36636q1mm1mmv41mmuu2eewi2eo1mw1mmuu1n6wi2ee3yi1mm3663xy2f81mm1mmve2ey2eo1mmuuv4v41mw366uu2ee1mw1ngvyv41mm1mmv41n62eevevo1n61mm1mmvyuuuu3y8v436g370uuv4uu1mw1ng36g370366uuuuv42eo3xyuu1mm4pq2eouuuu2eevo1mw1mm4pqv4v4veuuuuvouuvevouuvouuv43xy1n61mmvo1mwv4vouu1mm1mw366v41mmvo2eo3xyuuv42eyuuvouu2eouuv4ve2eo1mwuuuu1mm1mw1mm2eeuuv41n6v43yi2eev41mmwi1mmv437k1mmvo1mmuuv4ve3661mm1mw2eyve1ng1mmuuuu1n61mmuu69a3662eouuuu2gc4q01mmv42eeuu1mwuuuu1mmuuuu1mm370uu370uuuu2f81oa1mm1mmv44q0uuuuv41ng1nq3xy3xyv41mwuuuuv41mm2ee1mm3661mwvo1mwuuuu366vew8vovouuuuuuv4veuu3ys366uu2eev4v4veuu2ee5hi4pq36q1mmuu1mww8uuuuveve36gv4uuv4v4v4uuuuvy1mwuuveve1mm2eouuuuuuv4v4v43662ey1mw1mm1mmve1nquu2eo37kve1mwv4uuuu3xy69auu1mm3ys2eeveuuv41mm2eov41mwv41mw1mwuuv41mm2ee366vyv41mmv4v41n6uuv42f81mm4qa3662eouu2eeuu1mmuu1n6uuuuv41mmv4uu3y81mm2eeuuuu2eevove1mmuu1ngvev4uuvevo1mmv42eeveuuv41n6vyveuu36g1mmvevev4vy1n61mmw8uu2eyv4v4uu1mw1mwvew84q0ve1mm36qwiw8366uu1n6uuve1mmuu1mwvev4uu2eov41mw36q36g366v4uu2eeuuveuu37avyv4uu1mw36q1mm1mwuuveuuvo1mw2eeuuv41mw1ng3y8uu1mmv41mwvo1mmuuv42eove3661nguuv4uu1n61mm1mmvov4w81n6uu2ee2eo1nq36g4pq1mmuuuuvy1mw1mmuuuu3662eov4s65w5v33385w335w33gz8n8n5wbf358n34bfbf335xbf33gz5v8o61345v5w335x5v5v3536335v338n345v34gz3334bf338n345v33h034js346036345v8p378obg335w5v5v333335345v5w5vbg335w33375y33348nbg335w8q5x345v378s33608pbi8n348n353333335v5w8oeb335v338p5v8o335x5zgz5v33345w338n335v33338n3433335y3436e98o5w358o345w35335v5we78o3335bf5x345v8n33395w343533jrbf5v33355vbf33335v5v33345w5w33bf5v8o343334bfbg3334335v5v5v8q8p34335v335x365v33jr335w37355yed8n8n5v5v5v8q5x335w8n335y373335mj345v8o5x335x5v5w5w33343633bf8n5v333333373634365v338n335y5w33345x5v8n34348n608o5v355w335xgz34333333338n34e75y5vbg358n3433333333gz8p5zbgbg343335338n343633335x8n5z34335w335w33338o363333338n355x33345y5w353633h034333433365y8o338n8n5v5v338n338n8n5v353535bf5x338n345w33343334335vbf5v35348ne7345v5w3334365v33338n33335v5x33345z333333e7bf348n3533338n33h035338n34335v5v33358obf333534335v34pb5x398n34345y8n5y345x8n355v33348nbh5v5w5x342t1k51k5s3s3s31k5sn33zsn1jvs32bx1jv3vr1jv1jvsd1kp2bns3s3s3sx33z1k5sd4mz33f1k51kf3v7s33vrsx1jvs34nt2bxsd1jvsn3wlsn1kzsn1k55er34934jsx2bn1jvs31jvs3snsd1jvs31kf33psd2bnsds31jv33f2bx1k5sd2bx33ps31jv2bx1jv1jv2bnsn34tsdsd33zs3snsxsn1k51jvs3sds3sn33pt71jvs31jvsdsns32bn1k5s32c7s3s31kfths31jvs3s3s3s31jvs31jvs35fbs3sns32bnsd1jvs3sn349s31jvs32bn2bn1jv2bnsx33f33p1jvs3sn1jvs3tr1k52c71jv3w134tsds3s32c71jv33p1kfs3s3s3s333fs31jv1jv2bnsds32bn1kfs31jv3vh2crs31jvtrs32bns3snsdsx1k53vhs31jvsxths31k51jvs31k5sdsx2c7s3sd1kpsxsdsx1k5s31jv2bns31k5sd1jvs3sns33v71k5sn1kp1jvs31jv1kp1jvs32ch1jvsdsx2bnsnsd1jvsns32bx33p1jvsn2bns3t7s3s3s333f1kpsds3sdsx1kf2bns333fs32bn1kfs3sdsn1jv2ch2bn1jv1jv1jv1k5s334j1jvs3sds31k533z1jvsn2bn1jvt72bn1k51jvsn1jv2bxs32db1kfsnsns333psds31k51k52bx1jv3vr1l9s31jvsnsns32bnsd1k52c7sn349s31kp33zs3s31jvs32bn3v71k5sxsns333p1k52bx2bx2bx1jv1k5sdsd1kf1k5s3s333f2bxsdsxs31k5s31kfs333fsn2bn33fsxsds31k52d11kp1jvs334933p1k5sd2bnsxs3s3sdt71jvs3106xdulxexdxdxdulxeumuluu1o0uu1ng36g1mmvevouu366v4uu36qvovo3xyuuuu2eeuu1ngv41mmuu2eeuuuu1mm2eeuuveve1mmveuu1mw1mm2g2v4uu1nqw82eev41mmvo1mm4pq1mm1mmuuuuuuv42f81mmvovewiv4ve1mmve1mwv4v41n6uuuu36qvyuu1mm2eeuuv4uuuuuuveveve3y8v4v44qav4uu366ve1mwv4uuvyuuve1mmuuuuuu1mmv4ve3ys1n6vov41n6uuvyuu2eo2eyv4uu5hiuu4q0ve1ng1mw1nqvouuv41mmveuuvevouuve1mm2ee1mmveuu36guu1nq1mw1n6uu2eo1mm1n6ve69k5hiv4uuuuveuuuuvy36q1mw2eov4uu1mmuuv41n61mw36g1nguu1n61mmvovov41mm2eouuuuuu1mm1mm2ee2eeuuuuve3661nguuv43yiuu1mm1ng1mw1ngvouu1nquuve1mmveuu1mm1ng1mw1ngvouu1nquuve1mmveuu1mm1ng1mw1ngvouu1nquuve1mmveuu1mm1ng1mw1ngvouu1nquuve1mmveuu1mm1ng1mw1ngvouu1nquuve1mmveuu1mm1ng1mw1ngvouu1nquuve1mmveuu1mm1ng1mw1n61mm2eyvo5hi2ee1mm36guuw81mwuu2eo1n6uu1nguu1n61mm1mwuu1mm1ng1mw1nguu2eouuve3ysuu1mwuu1mmuuuuuuuuveuuvo5hiv41mm1nquuve36quuv41nqv41ou4qkuuve2ee1mw1mm5v5v33333333365v5w345y8n5wbf35335x365z345vbfe78p3633378n5v33mk365x348n33333534333333bf5x5v5y5w5z345w358n3336345y34335v36335we733e8335z5w8n37335z338n5z3534365v5w335v5y5w5ye8335w5w37345v348s5w5v363333638n345v35335x33gz335w345v5v8u5v378q34bg5v335w33343333ea33e78n3333355w5y5w5y35343333sd3v7s32ch1jvs3sd35dsn33fs3s3sd33psdt71jvsns31k5th3vh2c7sds32bns3s3s31jv1jvs31k5s32bns3th1jvs3s3u133f1kf2ch2chs333z1k52cr1kz2c7sdt7sdsn2bx4n91kp1jv1jvs3ths3sn1kf1l9sdsd4mz2bx1jv3vh33p1k5sd1kfsds33v7s333f1jv3vrsdsn2bn1jvsdsd1k52bn5f133ps3xeuqulupxeul10618huluoumulumxdxexhxd12xulul106ul105un106xdxdun12zum18o132ulxd107ulul18h105ul18h15qulxdulul15rum10yv4v4uuveuuuuv42eovev4uuuu2eovov41nqvyb'


def c(q):
    s = ''.join(sorted(set(string.digits + string.ascii_lowercase)))
    b = len(s)
    o = ''
    d = {i: j for i, j in zip(range(b), s)}
    while q:
        q, r = divmod(q, b)
        o = d[r] + o
    return o


c2m = {}
for i in range(1, 10):
    for j in range(1, 10):
        cur_s = f'{i}0{j}1'
        c2m[c(int(cur_s))] = cur_s
        cur_s = f'{i}1{j}0'
        c2m[c(int(cur_s))] = cur_s
        cur_s = f'0{j}1{i}'
        c2m[c(int(cur_s))] = cur_s
        cur_s = f'1{j}0{i}'
        c2m[c(int(cur_s))] = cur_s

for i in itertools.product(string.digits, repeat=4):
    cur_s = ''.join(i)
    if ('0' not in cur_s and '1' not in cur_s):
        continue
    cc = c(int(cur_s))
    if (len(cc) == 3):
        if (cc[0] > '2'):
            continue
    c2m[cc] = cur_s


def dfs(cur_string, cur_buf, cur_decoded, cur_bit):
    # vanish
    if (len(cur_buf) > 1):
        for i in range(1, min(3, len(cur_buf))):
            if (cur_bit == cur_buf[i]):
                geshu = cur_buf[:i]
                nxt_bit = '1' if cur_bit == '0' else '0'
                if (geshu[0] != '0'):
                    geshu = int(geshu)
                    dfs(cur_string, cur_buf[i + 1:], cur_decoded + cur_bit * geshu, nxt_bit)
    if (len(cur_buf) > 2):
        return
    # bigger
    if (cur_string == ''):
        if (cur_buf == ''):
            print('Aoligei!')
        return

    for i in range(3, 0, -1):
        if (cur_string[:i] in c2m):
            nxt_buf = cur_buf + c2m[cur_string[:i]]
            nxt_string = cur_string[i:]
            dfs(nxt_string, nxt_buf, cur_decoded, cur_bit)


def fail_gao(s):
    t = s
    m = ''
    while (t != ''):
        i = 3
        while (t[:i] not in c2m and i >= 0):
            i -= 1
        if (i <= 0):
            break
        m += c2m[t[:i]]
        t = t[i:]
        # print(i)
        # print(len(t))
        # raise Exception

    print(m)
    print(t)
    return m


def gao_2(s):
    t = s
    cur_decoded = ''
    cur_buf = ''
    cur_bit = '1'
    while (t != ''):
        i = 3
        while (i > 0):
            if (t[:i] not in c2m):
                i -= 1
                continue
            nxt_try_buf = cur_buf + c2m[t[:i]]
            nxt_try_decoded = cur_decoded
            nxt_try_bit = cur_bit
            print(nxt_try_buf)
            print(len(nxt_try_decoded))
            print(nxt_try_decoded[-40:])
            print(nxt_try_bit)
            print()
            # baosong
            skip_pattern = ['14071', '34071', '24071', '14051', '34051', '24051']
            if (nxt_try_buf in skip_pattern and nxt_try_bit == '0'):  # nxt_try_buf == '10015' and nxt_try_bit == '0'
                i -= 1
                continue
            elif (nxt_try_buf == '10011' and nxt_try_bit == '0'):  # nxt_try_buf == '10015' and nxt_try_bit == '0'
                nxt_buf = ''
                nxt_bit = '0'
                nxt_decoded = cur_decoded + '0' * 10 + '1'
                t = t[i:]
                break
            elif (nxt_try_buf == '100212' and nxt_try_bit == '0'):  # nxt_try_buf == '10015' and nxt_try_bit == '0'
                nxt_buf = '2'
                nxt_bit = '0'
                nxt_decoded = cur_decoded + '0' * 10 + '1' * 2
                t = t[i:]
                break
            elif (nxt_try_buf == '100211' and nxt_try_bit == '0'):  # nxt_try_buf == '10015' and nxt_try_bit == '0'
                nxt_buf = '1'
                nxt_bit = '0'
                nxt_decoded = cur_decoded + '0' * 10 + '1' * 2
                t = t[i:]
                break
            elif (nxt_try_buf == '311001' and nxt_try_bit == '1'):  # nxt_try_buf == '10015' and nxt_try_bit == '0'
                nxt_buf = '1'
                nxt_bit = '1'
                nxt_decoded = cur_decoded + '1' * 3 + '0' * 10
                t = t[i:]
                break
            elif (nxt_try_buf == '311003' and nxt_try_bit == '1'):  # nxt_try_buf == '10015' and nxt_try_bit == '0'
                nxt_buf = '3'
                nxt_bit = '1'
                nxt_decoded = cur_decoded + '1' * 3 + '0' * 10
                t = t[i:]
                break
            else:
                while (len(nxt_try_buf) > 2):
                    for j in range(1, min(3, len(nxt_try_buf))):
                        if (nxt_try_bit == nxt_try_buf[j]):
                            geshu = nxt_try_buf[:j]
                            nxt_bit = '1' if nxt_try_bit == '0' else '0'
                            int_geshu = int(geshu)
                            if (geshu[0] != '0' and (
                                    int_geshu < 30 or (int_geshu < 40 and len(nxt_try_decoded) > 200))):
                                nxt_buf = nxt_try_buf[j + 1:]
                                nxt_decoded = nxt_try_decoded + nxt_try_bit * int_geshu
                                break
                    else:
                        # shibai
                        i -= 1
                        break
                    nxt_try_bit = nxt_bit
                    nxt_try_buf = nxt_buf
                    nxt_try_decoded = nxt_decoded
                else:
                    # chenggong
                    nxt_bit = nxt_try_bit
                    nxt_buf = nxt_try_buf
                    nxt_decoded = nxt_try_decoded
                    t = t[i:]
                    break

        else:
            # shibai
            break
        cur_bit = nxt_bit
        cur_buf = nxt_buf
        cur_decoded = nxt_decoded

    print(len(t))
    print(t[:10])
    return cur_decoded


# dfs(s, '', '', '1')

# m = fail_gao(s)
# print(len(s))

print(len(s))
m = gao_2(s)
print(len(m))
m += '0' * ((8 - len(m)) % 8)

mm = long_to_bytes(int(m, 2))
with open('chall.png', 'wb') as f:
    f.write(mm)