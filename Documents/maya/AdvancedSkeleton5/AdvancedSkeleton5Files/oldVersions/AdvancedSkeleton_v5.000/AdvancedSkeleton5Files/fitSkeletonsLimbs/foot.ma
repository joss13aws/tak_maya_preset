//Maya ASCII 2012 scene
//Name: foot.ma
//Last modified: Mon, Jun 22, 2015 03:08:47 PM
//Codeset: 1252
requires maya "2008";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya 2012";
fileInfo "version" "2012 x64";
fileInfo "cutIdentifier" "001200000000-796618";
fileInfo "osv" "Microsoft Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -6.0287494776955661 4.4806963194858609 4.5598845648843174 ;
	setAttr ".r" -type "double3" -28.538352729648871 -56.599999999999078 2.8888882479088684e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".ncp" 1;
	setAttr ".coi" 7.2673653864153422;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -0.8551075417595414 0.16018051796912458 1.5299097133388109 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -0.91937106284165893 100.10324697418004 0.4916967164763465 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
	setAttr ".rp" -type "double3" 0 -2.2204460492503131e-016 -1.4210854715202004e-014 ;
	setAttr ".rpt" -type "double3" 0 -1.3988810110276976e-014 1.4432899320127038e-014 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ncp" 1;
	setAttr ".coi" 100.04519435800019;
	setAttr ".ow" 3.8596493843917434;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".tp" -type "double3" -0.88897224306076494 0.054805641999806198 1.4966241560389877 ;
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -1.1390155230779606 0.059977283645118562 100.10654101298519 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ncp" 1;
	setAttr ".coi" 100.1;
	setAttr ".ow" 4.2765088524135111;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.11303639011722 0.059977283645118562 0.65738656551887809 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ncp" 1;
	setAttr ".coi" 100.1;
	setAttr ".ow" 4.738876855570461;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "FitSkeleton";
	addAttr -ci true -sn "visCylinders" -ln "visCylinders" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "visBoxes" -ln "visBoxes" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "visBones" -ln "visBones" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "lockCenterJoints" -ln "lockCenterJoints" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "visGap" -ln "visGap" -dv 0.75 -min 0 -max 1 -at "double";
	addAttr -ci true -m -im false -sn "drivingSystem" -ln "drivingSystem" -at "message";
	addAttr -ci true -m -sn "drivingSystem_ToeCurl_R" -ln "drivingSystem_ToeCurl_R" -dv 1 
		-min 0 -max 1 -at "bool";
	addAttr -ci true -m -sn "drivingSystem_ToeCurl_L" -ln "drivingSystem_ToeCurl_L" -dv 1 
		-min 0 -max 1 -at "bool";
	setAttr -l on ".v";
	setAttr ".ove" yes;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".visBoxes" yes;
	setAttr ".visGap" 1;
	setAttr -s 30 ".drivingSystem";
	setAttr -s 15 ".drivingSystem_ToeCurl_R";
	setAttr -s 15 ".drivingSystem_ToeCurl_R";
	setAttr -s 15 ".drivingSystem_ToeCurl_L";
	setAttr -s 15 ".drivingSystem_ToeCurl_L";
createNode nurbsCurve -n "FitSkeletonShape" -p "FitSkeleton";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 29;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		2.3508348746736751 1.4394712022965405e-016 -2.3508348746736716
		-3.7929511823487981e-016 2.035719696933274e-016 -3.3245825626631635
		-2.3508348746736729 1.4394712022965413e-016 -2.3508348746736729
		-3.3245825626631635 5.899006384856358e-032 -9.6338085217116898e-016
		-2.3508348746736734 -1.4394712022965408e-016 2.350834874673672
		-1.0017616090771558e-015 -2.0357196969332745e-016 3.3245825626631644
		2.3508348746736716 -1.4394712022965413e-016 2.3508348746736729
		3.3245825626631635 -1.0933890203714376e-031 1.7856397797841755e-015
		2.3508348746736751 1.4394712022965405e-016 -2.3508348746736716
		-3.7929511823487981e-016 2.035719696933274e-016 -3.3245825626631635
		-2.3508348746736729 1.4394712022965413e-016 -2.3508348746736729
		;
createNode joint -n "Ankle" -p "FitSkeleton";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	addAttr -ci true -k true -sn "worldOrient" -ln "worldOrient" -min 0 -max 5 -en "xUp:yUp:zUp:xDown:yDown:zDown" 
		-at "enum";
	setAttr ".t" -type "double3" -1.0867024199147359 0.84983532411015528 -0.068643641764130958 ;
	setAttr ".ro" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 96.520886283829057 -6.3611093629270335e-015 -89.999999999999844 ;
	setAttr ".pa" -type "double3" 3.1147589914174403 -1.2104724556304993 -11.405913270501992 ;
	setAttr ".dl" yes;
	setAttr ".typ" 4;
	setAttr -k on ".fat" 0.36999999999999988;
	setAttr -k on ".worldOrient" 3;
createNode joint -n "Heel" -p "Ankle";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.36999999999999988 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.83962328905675265 -0.63936776490750791 0.073082862175327001 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.0888874903416268e-014 96.520886283828801 89.999999999998423 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Heel";
createNode joint -n "Toes" -p "Ankle";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.66611707946596865 1.371882183180767 -0.13086634227064525 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.88079466822934249 6.4613060347265385 82.220499038941597 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "PinkyToe1" -p "Toes";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" -0.17272346452771203 -0.023444560632726208 0.40392605231166079 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "PinkyToe2" -p "PinkyToe1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.22551338571312951 7.2164496600635175e-016 3.9968028886505635e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.8626838669297744e-006 1.3815119991060467e-005 -15.357691910328645 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "PinkyToe3" -p "PinkyToe2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.14551338571312744 3.3306690738754696e-016 -1.5543122344752192e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.99991516299653 0 0 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "RingToe1" -p "Toes";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" -0.059204846013090284 -0.0080361496100161411 0.28032197862075403 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "RingToe2" -p "RingToe1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.23730413361723146 3.8857805861880479e-016 1.1102230246251565e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.8626838422244779e-006 1.3815119945778259e-005 -15.357691910328651 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "RingToe3" -p "RingToe2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.1573041336172325 7.7715611723760958e-016 1.3322676295501878e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.99991516299661 0 0 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "MiddleToe1" -p "Toes";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.046845406502414866 0.0063585452973274337 0.13712217066583543 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "MiddleToe2" -p "MiddleToe1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.27494201662014195 4.4408920985006262e-016 2.4424906541753444e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.8626838430717271e-006 1.3815119891125552e-005 -15.357691910328695 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "MiddleToe3" -p "MiddleToe2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.19494201662014277 0 -1.5543122344752192e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.99991516299661 0 0 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "LongToe1" -p "Toes";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.046845163833335146 0.0063585123587217018 -0.05065162837998205 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "LongToe2" -p "LongToe1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.34999999999999831 4.9960036108132044e-016 1.1102230246251565e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.8626838542280486e-006 1.3815119905924891e-005 -15.357691910328651 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "LongToe3" -p "LongToe2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.27000000000000113 5.5511151231257827e-016 8.8817841970012523e-016 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.8626838959887427e-006 0 0 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ToesEnd";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "BigToe1" -p "Toes";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.046844868843391119 0.0063584723183587877 -0.27891055008907717 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "BigToe2" -p "BigToe1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.34999999999999742 3.8857805861880479e-016 7.7715611723760958e-016 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.8626838410561584e-006 1.3815119904745095e-005 -15.357691910328711 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "BigToe3" -p "BigToe2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.27000000000000091 2.2204460492503131e-016 3.3306690738754696e-016 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.8626838658931952e-006 0 0 ;
	setAttr ".typ" 5;
	setAttr -k on ".fat" 0.1;
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "FootSideOuter" -p "Ankle";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.83962328905672401 0.83362975682732954 0.39648837205973003 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 96.520886283829697 89.999999999995069 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "PinkyToe";
	setAttr -k on ".fat" 0.1;
createNode joint -n "FootSideInner" -p "Ankle";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29999999999999993 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.83962328905674133 0.73911786045122185 -0.43035198619317022 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 96.520886283829697 89.999999999995069 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "BigToe";
	setAttr -k on ".fat" 0.1;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode renderLayerManager -n "renderLayerManager";
createNode animCurveUA -n "SDK1FKBigToe2_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "bigCurl" -ln "bigCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKBigToe1_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "bigCurl" -ln "bigCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKBigToe2_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "bigCurl" -ln "bigCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKBigToe1_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "bigCurl" -ln "bigCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKLongToe2_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "longCurl" -ln "longCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKLongToe1_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "longCurl" -ln "longCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKLongToe2_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "longCurl" -ln "longCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKLongToe1_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "longCurl" -ln "longCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKMiddleToe2_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "middleCurl" -ln "middleCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKMiddleToe1_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "middleCurl" -ln "middleCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKMiddleToe2_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "middleCurl" -ln "middleCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKMiddleToe1_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "middleCurl" -ln "middleCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKRingToe2_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "ringCurl" -ln "ringCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKRingToe1_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "ringCurl" -ln "ringCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKRingToe2_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "ringCurl" -ln "ringCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKRingToe1_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "ringCurl" -ln "ringCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKPinkyToe2_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "pinkyCurl" -ln "pinkyCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKPinkyToe1_R_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "pinkyCurl" -ln "pinkyCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999892711639 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKPinkyToe2_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "pinkyCurl" -ln "pinkyCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK1FKPinkyToe1_L_rotateZ";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "pinkyCurl" -ln "pinkyCurl" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 17.99999893 0 0 10 -90;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKMiddleToe1_R_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 1.9999998807907111 0 0 10 -10;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKLongToe1_R_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 -0.19999998807907102 0 0 10 1;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKBigToe1_R_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 -6.5999996066093445 0 0 10 33;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKRingToe1_R_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 6.5999996066093445 0 0 10 -33;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKPinkyToe1_R_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 9.9999994039535522 0 0 10 -50;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKMiddleToe1_L_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 1.9999998809999999 0 0 10 -10;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKLongToe1_L_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 -0.1999999881 0 0 10 1;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKBigToe1_L_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 -6.599999607 0 0 10 33;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKRingToe1_L_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 6.599999607 0 0 10 -33;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode animCurveUA -n "SDK2FKPinkyToe1_L_rotateY";
	addAttr -ci true -sn "drivingSystemOut" -ln "drivingSystemOut" -at "message";
	addAttr -ci true -sn "spread" -ln "spread" -smn -2 -smx 10 -at "float";
	setAttr ".tan" 2;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -2 9.9999994040000004 0 0 10 -50;
	setAttr ".pre" 4;
	setAttr ".pst" 4;
createNode displayLayer -n "defaultLayer1";
createNode renderLayer -n "defaultRenderLayer1";
	setAttr ".g" yes;

select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av ".unw";
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;

connectAttr "SDK1FKBigToe1_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKBigToe2_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKLongToe1_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKLongToe2_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKMiddleToe1_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKMiddleToe2_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKRingToe1_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKRingToe2_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKPinkyToe1_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKPinkyToe2_R_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKMiddleToe1_R_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKLongToe1_R_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKBigToe1_R_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKRingToe1_R_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKPinkyToe1_R_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKBigToe1_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKBigToe2_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKLongToe1_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKLongToe2_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKMiddleToe1_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKMiddleToe2_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKRingToe1_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKRingToe2_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKPinkyToe1_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK1FKPinkyToe2_L_rotateZ.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKMiddleToe1_L_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKLongToe1_L_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKBigToe1_L_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKRingToe1_L_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "SDK2FKPinkyToe1_L_rotateY.drivingSystemOut" "FitSkeleton.drivingSystem"
		 -na;
connectAttr "Ankle.s" "Heel.is";
connectAttr "Ankle.s" "Toes.is";
connectAttr "PinkyToe1.s" "PinkyToe2.is";
connectAttr "PinkyToe2.s" "PinkyToe3.is";
connectAttr "RingToe1.s" "RingToe2.is";
connectAttr "RingToe2.s" "RingToe3.is";
connectAttr "MiddleToe1.s" "MiddleToe2.is";
connectAttr "MiddleToe2.s" "MiddleToe3.is";
connectAttr "LongToe1.s" "LongToe2.is";
connectAttr "LongToe2.s" "LongToe3.is";
connectAttr "BigToe1.s" "BigToe2.is";
connectAttr "BigToe2.s" "BigToe3.is";

connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[1]" "SDK1FKBigToe2_R_rotateZ.bigCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[0]" "SDK1FKBigToe1_R_rotateZ.bigCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[1]" "SDK1FKBigToe2_L_rotateZ.bigCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[0]" "SDK1FKBigToe1_L_rotateZ.bigCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[3]" "SDK1FKLongToe2_R_rotateZ.longCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[2]" "SDK1FKLongToe1_R_rotateZ.longCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[3]" "SDK1FKLongToe2_L_rotateZ.longCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[2]" "SDK1FKLongToe1_L_rotateZ.longCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[5]" "SDK1FKMiddleToe2_R_rotateZ.middleCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[4]" "SDK1FKMiddleToe1_R_rotateZ.middleCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[5]" "SDK1FKMiddleToe2_L_rotateZ.middleCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[4]" "SDK1FKMiddleToe1_L_rotateZ.middleCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[7]" "SDK1FKRingToe2_R_rotateZ.ringCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[6]" "SDK1FKRingToe1_R_rotateZ.ringCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[7]" "SDK1FKRingToe2_L_rotateZ.ringCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[6]" "SDK1FKRingToe1_L_rotateZ.ringCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[9]" "SDK1FKPinkyToe2_R_rotateZ.pinkyCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[8]" "SDK1FKPinkyToe1_R_rotateZ.pinkyCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[9]" "SDK1FKPinkyToe2_L_rotateZ.pinkyCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[8]" "SDK1FKPinkyToe1_L_rotateZ.pinkyCurl"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[10]" "SDK2FKMiddleToe1_R_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[11]" "SDK2FKLongToe1_R_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[12]" "SDK2FKBigToe1_R_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[13]" "SDK2FKRingToe1_R_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_R[14]" "SDK2FKPinkyToe1_R_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[10]" "SDK2FKMiddleToe1_L_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[11]" "SDK2FKLongToe1_L_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[12]" "SDK2FKBigToe1_L_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[13]" "SDK2FKRingToe1_L_rotateY.spread"
		;
connectAttr "FitSkeleton.drivingSystem_ToeCurl_L[14]" "SDK2FKPinkyToe1_L_rotateY.spread"
		;

// End of foot.ma
