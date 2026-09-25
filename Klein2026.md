PlasticityLossinDeepReinforcementLearning:ASurvey
TIMOKLEIN,FacultyofComputerScience,UniversityofVienna,AustriaandDoctoralSchoolComputerScience,
UniversityofVienna,Austria
CHRISTOPHLUTHER,IndependentResearcher,Austria
MANUSMCAULIFFE∗,MicrosoftAI,UnitedKingdom
LUKASMIKLAUTZ,DepartmentofMachineLearningandSystemsBiology,MaxPlanckInstituteofBiochemistry,
Germany
CLAUDIAPLANTandSEBASTIANTSCHIATSCHEK,FacultyofComputerScience,UniversityofVienna,
Austriaandds:UniVie,Austria
Plasticityreferstoanetwork’sabilitytoadapttochangingdatadistributions,whichiscrucialforthesuccessfultrainingofdeep
reinforcementlearningagents.Lossofplasticitycausesperformanceplateausandcontributestoscalingfailures,overestimationbias,
andinsufficientexploration.Todeepentheunderstandingofplasticityloss,weproposeaunifieddefinition,examineitsdriversand
pathologies,andorganizeover50mitigationstrategiesintothefirstcomprehensivetaxonomyofthefield.Ouranalysisshowsgapsin
currentevaluationpracticesandrevealsthatgeneralregularizationtechniquesoftenoutperformdomain-specificinterventions.Future
researchshouldprioritizeunderstandingthemechanismsunderlyingplasticityloss.
CCSConcepts:•Computingmethodologies→Reinforcementlearning;Neuralnetworks;Regularization.
AdditionalKeyWordsandPhrases:Plasticityloss,Capacityloss,Trainability
1 Introduction
DeepReinforcementLearning(RL)hasrecentlyseenmanysuccessesandbreakthroughs:Itbeatthebesthumanplayers
inGo[106]andDota[12],discoverednewmatrixmultiplicationalgorithms[35],endowedlanguagemodelswith
theabilitytogeneratehuman-likerepliesforbreakingtheTuringtest[14],andallowedforsubstantialprogressin
roboticcontrol[96].Itscapabilitiestoreacttoenvironmentalchangesandmakenear-optimaldecisionsinchallenging
sequentialdecision-makingproblemsarelikelycrucialforanygenerallycapableagent.Also,RL’scapabilitytolearn
purelyfromtrial-and-errormimicshumanlearning,makingitanaturalparadigmformodelinglearninginartificial
agents[108].
Despitealltheaforementionedsuccesses,deepRLisstillinitsinfancy,andcurrentmethodsareoftennotyet
reliableormature.Toreachhighlevelsofperformance,deepRLtypicallyneedssubstantialtweakingandelaborate
stabilizationtechniquesthatarenotoriouslydifficulttogetright:Fromreplaybuffersandtargetnetworksthatstabilize
temporal-differencelearning[85],tonoisedecorrelationandpessimisticvaluefunctionsthataddressoverestimation
bias[37,112],andfinallytoidiosyncraticoptimizersettingsandbespokehyperparameterschedulesthatmanage
gradientpathologies[4,79,103].
∗WorkdonepriortojoiningMicrosoftAI.
Authors’ContactInformation:TimoKlein,timo.klein@univie.ac.at,FacultyofComputerScience,UniversityofVienna,Vienna,AustriaandDoctoral
SchoolComputerScience,UniversityofVienna,Vienna,Austria;ChristophLuther,cph.luther@gmail.com,IndependentResearcher,Vienna,Austria;
ManusMcAuliffe,manusmcauliffe123@gmail.com,MicrosoftAI,London,UnitedKingdom;LukasMiklautz,DepartmentofMachineLearningand
SystemsBiology,MaxPlanckInstituteofBiochemistry,Martinsried,Germany;ClaudiaPlant;SebastianTschiatschek,FacultyofComputerScience,
UniversityofVienna,Vienna,Austriaandds:UniVie,Vienna,Austria.
Preprint 1
6202
rpA
81
]IA.sc[
3v23840.1142:viXra

2 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Therearemanyreasonswhythisisthecase:Firstandforemost,deepRLisinherentlynon-stationary,makingit
asubstantiallyharderlearningproblemthansupervisedlearning.Additionally,itsuffersfromitsownoptimization
issues,suchasunder-exploration,samplecorrelation,andoverestimationbias.Muchrecentworkhasbeendevotedto
tacklingtheseproblemswithincreasinglyelaboratealgorithms,manyofwhichaimtotransferinsightsfromtabularRL
tothedeepRLsetting[17,97].
Recentworksuggeststhatmanyoftheseissues—overestimationbias[88],scalingfailures[70],training
instability[39]—shareacommonrootcause:theoptimizationdifficultiesthatarisewhentrainingneural
networksonnon-stationarydata.Thisperspectivehasgainedtractionundertheumbrellatermplasticityloss.Indeep
learning,plasticityreferstoanetwork’sabilitytoquicklyadapttonewtargets;plasticitylosscharacterizesanetwork
stateinwhichthisabilityhasdegraded.BecausedeepRLagentscontinuouslyupdatetheirpoliciesandvalueestimates,
theyinducedistributionshiftsintheirowntrainingdata.Thesearepreciselytheconditionsunderwhichplasticityloss
occurs.EvidencesuggeststhatmitigatingplasticitylossalsoalleviatesclassicalRLchallenges:forinstance,applying
LayerNormandweightdecaystabilizesBaird’scounterexample[39],andfeaturenormalizationreducesoverestimation
biasincontinuouscontrol[88].Thelineofworkonplasticitylossaddressestwocentralquestions:
• WhydotheneuralnetworksofdeepRLagentslosetheirlearningability[30,78,79,88,91,107]?
• Howcantheabilitytolearnbemaintained[25,68,69]?
ThesequestionsmatterbeyonddeepRL:anysettingrequiringadaptationtochangingcircumstancesfacessimilar
challenges,includingcontinuallearning[30]andtheubiquitouspre-train/fine-tuneparadigminsupervisedlearning[11,
69].
Contributions. Thissurveymakesfourcontributions.First,weproposeaunifieddefinitionofplasticitylossthat
subsumes prior formalizations as special cases (Section 2). Second, we provide the first systematic taxonomy of
mechanisms,pathologies,andmitigationstrategies.Wecoverapproximately50methodsorganizedbymechanism
in Sections 4 and 5, summarized in Figure 2. Third, we identify a recurring empirical pattern by demonstrating
thatgeneral-purposeregularizationtechniquesfromsupervisedlearningconsistentlyoutperformdomain-specific
interventionsspecificallydesignedforplasticitypreservation.Fourth,wesynthesizeopenproblemsandmethodological
gaps,providingconcreterecommendationsforfutureresearch(Section6).
Scope. ThissurveyfocusesonplasticitylossindeepRL,withonlybriefdiscussionsofrelatedphenomenaincontinual
learningandsupervisedlearning.Existingcontinuallearningsurveys[116]addressplasticitylossonlyinconjunction
withcatastrophicforgettinganddonotfocusonRLasaprimarydomain.Consequently,theyexamineafundamentally
differentsetofmethodsandlackthedepthnecessaryforathoroughunderstandingofplasticitylossindeepRL.
OurworkalsodiffersfromKhetarpaletal.[62]’ssurveyoncontinualRL,whichaddressesbroadertopicssuchas
creditassignmentandskilllearning.WeemphasizeconnectionsbetweenplasticitylossandotherdeepRLchallenges,
includingoverestimationbias[88]andscalingfailures[34].WithindeepRL,weconcentrateonthesingle-agentsetting,
wheretheunderstandingofplasticitylossismostdeveloped.
Structure. Section2introducesnotation,theRLformalism,andourunifieddefinitionofplasticityloss.Section3
positionsourworkrelativetocontinuallearningandcontinualRL.Section4categorizespotentialmechanismsand
symptomsofplasticityloss,andSection5presentsataxonomyofmitigationstrategies.Weconcludewithadiscussion
ofopenproblemsandfuturedirectionsinSection6.
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 3
2 NotationandPreliminaries
Wenowintroduceournotation,brieflyoutlinethebasicsofRL,andpresentkeyRLquantitiesrelevanttoplasticityloss,
alongwithourunifyingdefinitionofthelatter.Finally,Section2.4reviewsbenchmarksusedtostudyplasticityloss.
2.1 GeneralNotation
Weadoptthefollowingnotation:Weuselower-caseboldsymbolsforvectors,e.g.,x∈X ⊆R𝑑′ todenoteaninput
samplefromthedataspaceXofdimension𝑑′.Upper-caseboldsymbolsdenotematrices,e.g.,X∈R𝑛×𝑑′ denotesthe
designmatrixwhoserowscontainsamplesfromX.Expectationswithrespecttoadistribution𝑃aredenotedasE a∼𝑃[·].
Ifitisclearfromthecontext,weskipthesubscriptforbrevity.WeuseSVD(A)todenotethemultisetofallsingular
valuesofA,𝜎 todenoteasinglesingularvalue,𝜎 𝑖(A)todenotethe𝑖thlargestsingularvalueofmatrixAand𝜎
min
and𝜎
max
todenotethesmallestandlargestsingularvalue,respectively.For𝜙:R𝑑′ →R𝑑 beingafunctionmapping
samplestofeatures,wedenotethefeaturematrixas𝜙(X) ∈R𝑛×𝑑,where𝑑isthedimensionoftherepresentation.
2.2 ReinforcementLearning
InRL,thegoalistooptimizetherewardreceivedfromanenvironmentafterperforminganaction.Thisinteractive
processisformalizedviaMarkovDecisionProcesses(MDPs)describedbytuplesM =(S,A,P,𝑟,𝜌
0
,𝛾),whereSis
thestatespace,Aisthesetofpossibleactions(actionspace),P:S×S×A→ [0,1]atransitionkernelspecifying
theprobabilityoftransitioningfromonestatetoanotherupontakingaspecificaction,𝑟:S×A→Risthereward
functionspecifyingtherewardtheagentobtainsfortakinganactioninastate,𝜌 istheinitialstatedistribution,and𝛾
0
istheso-calleddiscountfactor.Thepossiblystochasticpolicy𝜋:S→ [0,1]|A| specifiesforeachstateadistribution
overtheactionsandthusdeterminestheagent’sbehavior.Weoftenwrite𝜋(𝑎|𝑠)todenotetheprobabilityofaction𝑎
instate𝑠accordingtopolicy𝜋.Theagentaimstomaximizethe(discounted)cumulativereward
(cid:34) ∞ (cid:35)
𝐽(𝜋)=E ∑︁ 𝛾𝑡𝑟(𝑠 𝑡 ,𝑎 𝑡) , (1)
𝑡=0
whereactionsaretakenaccordingtotheagent’spolicy𝜋 andtheexpectationisovertherandomnessofthetransitions,
theagent’spolicy,andtheinitialstate.Anoptimalpolicy𝜋∗maximizes𝐽(𝜋).KeyquantitiesforRLalgorithmsarethe
state-value,
(cid:34) ∞ (cid:35)
𝑉𝜋(𝑠)=E ∑︁ 𝛾𝑡𝑟(𝑠 𝑡 ,𝑎 𝑡) |𝑠 0=𝑠 , (2)
𝑡=0
i.e.,theexpectedcumulativerewardwhenstartingfromstate𝑠andfollowingpolicy𝜋 fromthere,andtheaction-value,
(cid:34) ∞ (cid:35)
𝑄𝜋(𝑠,𝑎)=E ∑︁ 𝛾𝑡𝑟(𝑠 𝑡 ,𝑎 𝑡) |𝑠 0=𝑠,𝑎 0=𝑎 , (3)
𝑡=0
i.e.,theexpectedreturnstartingfromstate𝑠,takingaction𝑎,andfollowingpolicy𝜋 afterwards.Anoptimalpolicycan
befoundbymaximizingtheexpectedvalueoftheinitialstate,i.e.,
𝜋∗ ∈argmax E [𝑉𝜋(𝑠)] (4)
𝜋 𝑠∼𝜌0
Preprint

4 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Notethatstate-values(and,similarly,action-values)canalsobedefinedrecursively:
𝑉𝜋(𝑠)= E [𝑟(𝑠,𝑎)+𝛾 ∑︁ P(𝑠,𝑠′,𝑎)𝑉𝜋(𝑠′)], (5)
𝑎∼𝜋(𝑠)
𝑠′
Inspiredbytheserecursivedefinitionsareso-calledTemporal-Difference(TD)learningapproaches,e.g.,approaches
basedoniterativelyupdatingstate-valueestimatesas
𝑉ˆ𝜋(𝑠 𝑡)←𝑉ˆ𝜋(𝑠 𝑡)+𝛼[𝑟 𝑡 (cid:32)+(cid:32)(cid:32)(cid:32) 1 (cid:32)(cid:32)(cid:32)(cid:32)(cid:32) + (cid:32)(cid:32)(cid:32)(cid:32)(cid:32) 𝛾 (cid:32)(cid:32)(cid:32)(cid:32) 𝑉 (cid:32) ˆ (cid:32)(cid:32)(cid:32)(cid:32) 𝜋 (cid:32)(cid:32)(cid:32)(cid:32) ( (cid:32) 𝑠 𝑡+(cid:32) 1 (cid:32)(cid:32)(cid:32) ) (cid:32)(cid:32)(cid:32)(cid:32) − (cid:32)(cid:32)(cid:32)(cid:32)(cid:32) 𝑉 (cid:32)(cid:32) ˆ (cid:32)(cid:32)(cid:32)(cid:32) 𝜋 (cid:32)(cid:32)(cid:32)(cid:32) ( (cid:32)(cid:32) 𝑠 (cid:32)(cid:32) 𝑡 (cid:32) )]. (6)
(cid:124) (cid:123)(cid:122) (cid:125)
TDerror
Inshort,estimatesofstate-oraction-valuesareupdatedbasedonestimatesoffuturestates(andactions),whichiswhy
suchmethodsarealsocalledbootstrappingmethods.ThetermwithinbracketsisalsoreferredtoasTDerror.
IndeepRLagents,𝑉𝜋,𝑄𝜋 or𝜋(orcombinationsofthose)arerepresentedbydeepneuralnetworks.Manyworks[48,
76]decomposeadeepRLagentintoalearnedrepresentation𝜙,coveringalllayersuptoandincludingthepenultimate
layer,andalineartransformationW.ThisallowsviewinganRLagent’spolicyorvaluefunctionasalinearfunctionof
somelearnednon-linearfeaturesobtainedthroughanon-lineartransformationofthestates𝜙(𝑠)orcorresponding
observations.Usingthevaluefunctionasanexample,ournotationforthisdecompositionis𝑉(𝑠)=⟨𝜙(𝑠),W⟩.
2.3 DefinitionofPlasticityLoss
Intheliterature,plasticitylosslacksaunifieddefinition.Here,weconsolidateexistingdefinitionsanddemonstratethat
manyprioronesariseasspecialcasesofourformulation.Intuitively,allaimtoquantifyamodel’sdiminishedabilityto
fitnewtargetsbutdifferinhowtheyformalizethisandtheirtraining-evaluationsetup.Ourunifieddefinitionreads:
Definition2.1(Lossofplasticity). Let𝑃(𝑡) beadistributionoverinputsinXandtargetsinY,andlet𝐿(1),𝐿(2),...
X,Y
beasequenceofreal-valuedlossfunctionswithdomainX×Y.Let𝑔
𝜃
representaneuralnetworkwithparameters𝜃,
Ocorrespondtoanoptimizationalgorithm,potentiallywithanoptimizationbudget,andIrepresentanintervention
ontheparameters𝜃.Wedenotethelossoftheneuralnetworkattime𝑡 usingparameters𝜃 as
𝑐(𝑡)(𝜃)=E
(x,y)∼𝑃
X
(𝑡
,Y
)
(cid:2)𝐿(𝑡)(𝑔 𝜃(x),y) (cid:3). (7)
Basedonthis,wedefinethelossofplasticityas
C({𝑃(𝑡) }𝑇 ,{𝐿(𝑡)}𝑇 ,O,I)=𝑐(𝑇)(O(𝜃(𝑇)′,𝑃(𝑇),𝐿(𝑇)))−𝑐(𝑇)(𝜃˜(𝑇)) (8)
X,Y 𝑡=1 𝑡=1 X,Y
where
𝜃(𝑡+1) =O (cid:16) 𝜃(𝑡)′,𝑃(𝑡) ,𝐿(𝑡) (cid:17) , 𝜃(𝑡)′ =I(𝜃(𝑡),𝑃(𝑡) ,𝐿(𝑡)), and 𝜃˜(𝑡) =O (cid:16) 𝜃init,𝑃(𝑡) ,𝐿(𝑡) (cid:17) . (9)
X,Y X,Y X,Y
Here𝜃initdenotesrandominitialparameters.
Thisdefinitiongeneralizesmanyexistingdefinitionsinthatitenablesdifferentlossesatdifferenttimesteps,which
is,e.g.,relevantformulti-tasklearning,andinthatitallowsforexplicitmanipulationsoftheparametersoutsideof
thebehavioroftheoptimizationalgorithm.1Notethatourdefinitionfocusessolelyonfinal-taskperformance.This
isincontrastwithmetricscommonlyusedincontinuallearning,suchasaverageaccuracy[116],whichaggregate
performanceoveralltasks.
1Interventionsontheparameters,e.g.,resettingparameterstorevivedeadneurons,couldalsobeconsideredaspartoftheoptimizer.However,making
theinterventionsexplicitandnotconsideringthemaspartoftheoptimizercanhelpclarifythedifferentmechanismsthataffectlossofplasticity.
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 5
Manydefinitionsoflossofplasticityintheliteraturearespecialcasesoftheabovedefinition,thoughsomeauthors
refertothisphenomenonbydifferentterms:
• Berariuetal.[11]definedthegeneralizationgapas“thedifferenceinperformancebetweenapretrainedmodel
(e.g.,onethathaslearnedafewtasksalready)versusafreshlyinitializedone”.Thenotionofthealready-learned
taskscorrespondstodifferenttasksgivenby𝑃(𝑡) ,𝐿(𝑡) for𝑡 =1,...,𝑇 −1whiletheperformanceisevaluated
X,Y
withrespecttoafinaltaskcharacterizedby𝑃(𝑇),𝐿(𝑇).Thefreshlyinitializedmodelisgivenby𝑔 with𝜃(0)
X,Y 𝜃(0)
beingrandominitialparameters.
• Lyleetal.[75]definedthetarget-fittingcapacityasameasureofhowwellaneuralnetworkcanfitadistribution
oftargetsgivenbyafamilyoflabelingfunctions(real-valuedfunctionsmappinginputsfromXtotargets).This
definitionarisesfromDefinition2.1byconsidering𝑇 =1andselecting𝑃(𝑡) ,𝐿(𝑡) accordingly.2
X,Y
• Lyleetal.[79]alsodefinelossofplasticity butdonotexplicitlyaccountfortime-dependentdistributions
𝑃(𝑡) ,𝐿(𝑡) and interventions. Their definition is thus a special case, where no intervention is applied and
X,Y
constantdistributionsareusedforboththeinputandthelossfunctions.
• Elsayed and Mahmood [30] provide a sample-based notion of plasticity loss corresponding to a baseline
normalizedversionoftheplasticitylossdefinedinLyleetal.[79].Theirdefinitionarisesasaspecialcaseof
oursbyfixingthelossfunction(i.e.,usingthesamelossfunctionsforall𝑡)whilemakingitdependentonthe
optimizerandtheintervention.
2.4 CommonBenchmarksinDeepReinforcementLearningandPlasticityLoss
Plasticitylosscanarisenaturallyduringlearningorbeartificiallyinducedforstudybyartificiallyinjectingnon-
stationarityintoastationarylearningproblem.Accordingly,benchmarkscanbecategorizedintotwotypes:RLenvi-
ronmentswithinherentnon-stationarityandsupervisedlearningdatasetswithartificiallyintroducednon-stationarity.
RLBenchmarks. Table1listsRLbenchmarksforplasticityloss.Themostwell-establishedareAtari[10](discreteac-
tions,imageobservations)andDeepMindControlSuite(DMC)[109](continuousactions,imageorvectorobservations).
Bothbenchmarkscontaindiversesetsofenvironments,includingoneswhereplasticitylossoccursstrongly.ForAtari,
differentgamesubsetshavebeenidentifiedwhichexhibitplasticityloss,withcommonlystudiedexamplesincluding
Phoenix,SpaceInvaders,Seaquest,DemonAttack,andAsterix[23,90,107].ForDMC,Naumanetal.[88]identify
theDogenvironmentasparticularlychallengingduetoexplodinggradientsduringtraining.Additionalbenchmarks
includeAtari-100k[61],a26-gamesubsetthatexacerbatesplasticitylossthroughhighreplayratios(manygradient
updatesperenvironmentstep)[26,91],andMuJoCo[110],whichhaslargelybeensupersededbyDMC.
Table1. DeepRLbenchmarksforplasticityloss.
Benchmark Introducedby
Non-stationaryMuJoCo[110] Dohareetal.[24]
DeepMindControlDog[109] Naumanetal.[88]
Atari[10]subset:Phoenix,Yarsrevenge,Surround,Seaquest,Alien,Enduro,Asteroids,Gopher Nikishinetal.[90]
Atari[10]subset:Demonattack,Asterix Sokaretal.[107]
Atari[10]subset:Asterix,Enduro,Qbert,Jamesbond,Seaquest,Timepilot Delfosseetal.[23]
Atari-100k[61] Nikishinetal.[91]
2ThereisstillaslightdifferencebetweenthedefinitioninLyleetal.[75]andourdefinition:ourdefinitionsubtracts𝑐(𝑇)(𝜃(0))asabaseline.
Preprint

6 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Table2. Syntheticbenchmarksforplasticityloss.
Benchmark Non-stationarity Introducedby
Non-stationaryMNIST Pixelshuffling,Labelshuffling,Labelnoise,Smalldata Goodfellowetal.[44],Lyleetal.[79],Leeetal.[69]
Non-stationaryCIFAR10 Labelnoise,Labelshuffling,SmallData Igletal.[56]
Non-stationaryImageNet Classificationsequence,Labelshuffling,Labelnoise, Dohareetal.[24],ElsayedandMahmood[30],Leeetal.
Smalldata [69]
Largetargetregression High-frequencytargets Lyleetal.[78]
SyntheticBenchmarks. Table2showssyntheticbenchmarksthatartificiallyinducenon-stationarityinsupervised
datasets.Commonapproachesinclude:(1)inputshifts viapixelshuffling[24]),(2)labelshifts throughconsistent
permutation[79]orrandomnoise[56,69],and(3)datascarcitythroughreduceddatasetsize[69].Thesemodifications
havebeenappliedtoMNIST,CIFAR-10,andImageNet.ContinualImageNet[24]isacomplementarybenchmarkusing
sequentialbinaryclassificationtasksdrawnfromImageNet’s1000classes.Allofthesemodificationscanalsobeapplied
inwarm-starting settings,whereanetworkispre-trainedwithnon-stationarydataandthenfine-tunedonclean
data.Thissetupmirrorstheubiquitousfine-tuningparadigmforpre-trainedmodelsandtestswhetherearlytraining
conditionsdegradeplasticity[11,29,69,78].Lastly,Lyleetal.[78]notethatvalue-basedRLusesregressionratherthan
classification[46,85],anddeveloparegressionbenchmarkwithoscillatinglarge-meantargets,betterreflectingRL
optimizationchallenges.
3 RelatedWork
PlasticitylossindeepRLoverlapswithtwocloselyrelatedfields:continuallearningandcontinualRL.Continual
learningaddressesscenarioswheremodelslearnincrementallyfromchangingdatadistributionsortasks,typically
emphasizingthestability-plasticitytrade-offtomitigatecatastrophicforgetting[116].Recentcomprehensivesur-
veysoutlinetheoreticalfoundations,categorizemethodologicalapproaches(e.g.,regularization-based,replay-based,
architecture-based),andhighlightpracticalapplicationsacrossvarieddomains[6,116].Specifically,theadaptationand
continualfine-tuningoflargelanguagemodelsposeadvancedchallengesofcontinuallearning,requiringadaptation
fromgeneraltospecificcapabilitiesaswellasadaptationacrosstime[105].
Incontrast,thissurveyspecificallyfocusesonplasticitylosswithindeepRL,whereshiftsinthedatadistribution
naturallyarisewithoutexplicittaskboundaries.Suchnon-stationarityarisesinherentlyduetopolicyupdatesor
improvedvalueestimates,whichaffecttheagent’sinputandtargetdistributions.Unlikecontinuallearning,catastrophic
forgettingisnotcentralhere;rather,theemphasisisexclusivelyonanetwork’scapacitytocontinuallyupdateparameters
inresponsetoevolvinglearningsignals[4,78,90].Thus,evenstationaryenvironmentscanexhibitsignificantplasticity
loss,distinguishingdeepRLfromclassicalcontinuallearning.
Continual RL addresses non-stationarity from internal policy changes and external dynamics in transition or
rewardfunctions.Thissettingintroduceschallengessuchasexploration,creditassignment,andgoal-conditioned
learning[2,62].Ourscope,however,specificallytargetsplasticitylossindeepRL.Wefocusontheagent’sdiminished
abilitytotrainandadapt,excludingbroaderissuesintegraltocontinualRL.
4 DriversandPathologiesofPlasticityLoss
Thissectioncategorizesthecontributingfactorsofplasticitylossidentifiedintheliterature.AsvisualizedinFigure1,
wedistinguishbetweendriversandpathologies.Driversencompasshigh-levelpropertiesofthelearningproblemor
algorithmicchoicesthatinduceplasticityloss,suchasenvironmentproperties(Section4.1),non-stationarity(Section4.2),
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 7
Replayratio (Large-mean) Dead
scaling regression Neurons
Large Loss
Environment Input/Output Unstable Reduced
parameter landscape
properties non-stationarity gradients Performance
norms sharpness
Legend Rank
Collapse
Non-Measurable Measurable
Driver Pathology
Fig.1. Possibleconnectionsbetweendriversandpathologiesofplasticitylossinvalue-basedRL.Large-meanregression
targets,combinedwiththenon-stationarityofdeepRLtraining,causelargeandunstablegradients,leadingtoanincreasein
parameternorms.Largeparameternormsareknowntoincreaselosslandscapesharpnessandcauseotherpathologies,together
leadingtoreducedagentperformance.
highreplayratios(Section4.3),andtheobjectivefunction(Section4.4).Pathologiesdescribetheresultinginternal
networkstatesoroptimizationdynamicsassociatedwithlostplasticity.Wereviewthesedownstreameffects,including
parameternormgrowth(Section4.5),representationrankcollapse(Section4.6),andsaturatedunits(Section4.7).
Finally,wediscussoptimization-specificpathologies,suchasgradientinstability(Section4.8),losslandscapecurvature
(Section4.9),andearlyoverfitting(Section4.10).
4.1 EnvironmentProperties
DeepRLbenchmarksexhibitsubstantialvariationinplasticityloss,suggestingthatenvironment-specificpropertiesare
causalfactors.Anexampleofthisischangingenvironmentdynamicsovertime.Ataricanbecategorizedintostationary,
dynamic,orprogressivegames,dependingonhowtheirinputdistributionsevolve[23].“Stationary”gameschangelittle
ornotatall,“dynamic”gamesshiftindependentlyoftheagent(e.g.,newgearinAsterix),and“progressive”games
adapttotheagent’sprogress,asinJamesBondandMontezuma’sRevenge.Anotherexampleofchangingenvironment
dynamicsisprocedurallygeneratedbenchmarkssuchasProcGen,whichintroducevariabilitybyindividuallygenerating
eachlevel[22].Notably,thesechangesdonotaffectallalgorithmsequally:off-policymethodslikeDQN,whichstore
pasttransitionsinareplaybuffer,aretypicallymoresensitivethanon-policymethodssuchasPPO[27].
Targetnon-stationarityinducedbytheenvironmentmayalsoplayarole:itcanincreasegradientnormsandreduce
plasticity[78,89].InAtari’sSeaqest,forinstance,rewardmagnitudesgrowasthegameprogresses[10].Reward
clippingmitigatesthisgrowthbutpotentiallydiscardsusefulsignals[85].DogandHumanoidenvironmentsofthe
DeepMindControlSuite[109]arecontinuous-controltaskswithhigh-dimensionalactionspaces,whichaddsadifferent
layerofdifficulty.Theseenvironmentscauseplasticitylossbygeneratinglarge,divergentgradients[88,89].While
regularizationcanmitigatelarge-magnitudegradients,itisnotguaranteedthatregularizationstrategiessucceedingin
onesuite(e.g.,DMControl)alsosucceedinothers(e.g.,MetaWorld)[88].
Preprint

8 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
4.2 Non-stationarity
Non-stationarityissimultaneouslythemostlikelyculpritforcausingplasticitylossandoneofthemostelusive[24,
56,68,69,75].However,determiningpreciselyhowandwhyitaffectslearningremainschallenging,mainlydueto
difficultiesquantifyingthedegreeofnon-stationarity.Inthefollowing,weexaminedifferentaspectsofnon-stationarity
thatmaycontributetoplasticityloss.
InputNon-stationarityisdefinedthroughchangesintheinputdatadistribution𝑃(x)[68].IndeepRL,thisoften
occursduetoachangingpolicythatgeneratesdatafromaslightlydifferentdistributionwitheachupdate.Input
distributionshiftsmayrequireneuralnetworkstore-learnrepresentationsentirely,ataskatwhichtheytypically
struggleduetolimitedplasticity[30].Thismismatchbetweentheneedtore-learnunderdistributionshiftsandthe
network’slimitedadaptivecapacitycancontributetoplasticityloss[30].Inexperiments,suchshiftscanbeinduced
bypermutinginputpixelsorbyprogressivelyexpandingdatasets[56,68,69,78](cf.Section2.4).Theseverityof
performancedegradationtypicallycorrelateswiththeextentofthedistributionshift.Wheninitiallylearningonsmaller
subsetsofdata,theseshiftscancausenetworkstooverfit,whichdamagessubsequentlearningandgeneralization.This
damagepersistsdespitelaterexposuretoacompletedataset[56,69,78].
TargetNon-stationarityoccurswhenthelabeldistribution𝑃(𝑦|x)changes[68].IndeepRL,thisnaturallyoccurs
withtemporaldifferencelearningduetobootstrapping(cf.Section2.2).Multiplestudiesindicatethattargetnon-
stationaritydrivenbybootstrappingsignificantlycontributestoplasticitylossbycausingissuessuchasrepresentation
collapse[65],growingparameternorms[78],earlyperformancecollapse[80],ordormantneurons[107].Allthese
pathologiesareassociatedwithdegradedlearningperformance.However,theliteratureisconflictingontheprecise
roleoftargetnon-stationarity.Sokaretal.[107]observeddormantneuronseveninofflineRLsettings,suggesting
targetnon-stationarityhasamoreprominentrolethaninputnon-stationarityinplasticityloss.Incontrast,Elsayed
andMahmood[30]arguethattargetnon-stationarityrelatesmorecloselytocatastrophicforgettingthanplasticity
loss,asadjustingtolabelchangestheoreticallyrequiresupdatingonlytheoutputlayerratherthanfullyre-learning
representations.
TrainabilityandGeneralizabilityaretwodistinctyetinterconnectedaspectsofnetworkplasticityloss[60,69].
Leeetal.[69]examinefine-tuningofpre-trainedmodels(warm-starting)undernon-stationarity.Theyfindthatwhile
warm-startedmodelsmaintainhightrainingaccuracy,thenon-stationarityaffectsgeneralizabilityasmeasuredby
testerror.However,theauthorsarenotabletoestablishadefinitivemechanismlinkingnon-stationaritydirectlyto
plasticityloss[69].Inanotherstudy,JulianiandAsh[60]investigateplasticitylossspecificallywithinon-policyRL
usingPPO,analyzingvarioustypesofnon-stationarity.Theirfindingsindicateacleardegradationinbothtraining
andtestingperformanceasnon-stationarityincreases.IncontrasttoLeeetal.[69],JulianiandAsh[60]establisha
linkbetweennon-stationarityandrisingparameternorms,suggestingthatparametergrowthnegativelyimpactsboth
trainabilityandgeneralizability.
Insummary,thereisoverwhelmingevidencethatnon-stationarityisacrucialfactorinplasticityloss,although
theprecisemechanismsremainunclear[77,78].Webelievethatfocusingmorenarrowlyonspecificformsofnon-
stationarity,suchastargetshifts[68],ispromisingforunderstandingthemechanismslinkingnon-stationarityand
plasticityloss.Clarifyingthesemechanismshasthepotentialtoadvanceboththetheoreticalfoundationsandpractical
solutionstoplasticitylossindeepRL.
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 9
4.3 HighReplayRatioTraining
OptimizationhyperparametersplayacriticalroleinthetrainingdynamicsofdeepRLagentsandhaveasignificant
impactonthephenomenonofplasticityloss.Amongthese,thereplayratio(RR),sometimesalsocalledtheupdate-to-data
(UTD)ratio,isarguablythemostimportanthyperparameteraffectingplasticityloss.
TheRRdescribesthenumberofgradientupdatesperenvironmentstep[18,91]foroff-policydeepRLagents.
Forinstance,theoriginalDQNagentutilizesRR=0.25,meaningonegradientstepforeveryfourenvironmentsteps
[85],whereasSACemploysRR=1[46].WhilehigherRRscanofferimprovedsampleefficiency,manyalgorithmsdo
notleveragethemduetoobservedperformancedegradationandtheemergenceofdegeneratepolicies[26,91].This
degradationhasbeenattributedtooverfittingonearlysamples[91]or,morerecently,earlyplasticityloss[26].Ma
etal.[80]hypothesizethatelevatedRRsexacerbateinitialtargetnon-stationarity,whichinturnleadstoagentslosing
plasticityprematurelyduringtraining.AcommoninterventiontomitigatetheadverseeffectsofhighRRtraining
inoff-policydeepRListheapplicationofresets,whichhavedemonstratedefficacyacrossarangeofbenchmarks
[26,88,89,91,103].
Inourview,itisunlikelythathigh-replayratiotrainingisthemaincauseofplasticityloss.Plasticitylossalso
manifestsinscenarioswithouthighRRtraining,suchaswithastandardDoubleDQNagentonAtarigameslike
PhoenixandSpaceInvaders[90].ItappearsthathighRRsamplifyplasticitylossratherthandirectlycausingit,which
issupportedbyNaumanetal.[88],whonotethathighRRsinducedistincttrainingdynamicscomparedtolowRRs.A
prominentexampleisDeepMindControl’sDogenvironment,whereSACagentswithhighRRssufferfromexploding
gradients[88].RemediesfortheamplifyingeffectofhighRRsonplasticitylosscanbefoundinSections5.1,5.3,5.4,5.8,
5.11and5.12.
Beyondthereplayratio,otheroptimizationhyperparameterssignificantlyinfluenceplasticity.Largerlearningrates
canaidinescapingsuboptimallocalminimainsupervisedlearning,whereasinofflinedeepRL,highlearningrates
arepronetorankcollapseanddeadneurons[45].Implicitlearningrateschedulingmayalsoplayalargerrolethan
previouslythought[77],underscoringtheneedforcarefultuning.Thetotalnumberoftrainingstepsintuitivelyimpacts
plasticity:longertrainingononetaskcanleadtoreducedadaptabilityforsubsequenttasks[73].Finally,thebatchsize
interactswithbothgradientnoiseandlearningrate:smallerbatchescanreducegradientcollinearityandsometimes
improveperformance[93],whilelargerbatchessupportstabilityathigherlearningratesbutmayalsoincreasetherisk
ofdeadunits[45].Therefore,empiricallytuninghyperparametersforagiventaskandenvironmentisoftennecessary
toachieveoptimalperformanceandplasticity[92].
4.4 ObjectiveFunction
ClassificationtaskshavebeenobservedtobeeasierfordeepneuralnetworksthanregressioneversincetheAlexNet
breakthroughinimageclassification[34].Becausevalue-baseddeepRLmethodsusearegressionloss,recentworkhas
hypothesizedthatregressingonnon-stationarytargetsmightbeoneoftheleadingcausesofdeepRL’soptimization
issues[34,78].Forexample,thetwo-hottrick[101]hasbeensuccessfullyappliedtotrainvaluenetworksandhas
since been linked to mitigating plasticity loss, albeit at a performance cost [79]. Farebrother et al. [34] find that
reformulatingregressionasclassificationusingamethodcalledHL-Gauss[57]improvesRLagentsinmanyways,such
asrepresentationalcapacity,robustnesstonoiseanduncertainty,andsampleefficiency.However,theydonotprovide
deeperinsightsintotheexactmechanismsbehindregressionoptimizationissues.
Preprint

10 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Arecentinvestigationintothemechanismsdrivingplasticitylosshypothesizesthatregressionwithlarge-mean
targetscausesnetworkstoloseplasticityeveninstationarylearningproblems[78].Thisissueisparticularlyprevalent
invalue-baseddeepRL,whereanagentideallyimprovesthroughouttraining,resultingintemporaldifferencetargets
withincreasingmagnitude.Regressingonlarge-meantargetshastwonegativesideeffects:First,deepnetworksare
pronetoencodingthetargetoffsetintotheirweightsinsteadofthebias.Thisleadstoanexplosionofthesingular
valuesofthecorrespondingdimensionsinparameterspace,resultinginanill-conditionedfeaturematrix[78].Second,
whenthenetworkpredictsthelarge-meantargetsinsufficientlywell,thesquaringinthemeansquarederroryields
largeerrorterms.Asgradientsareproportionaltoerrorsinregressiontasks,theselargeerrorspotentiallycausethe
parameternormsofthenetworktogrowrapidly[34,78].Thisgrowthoftheparameternormsisassociatedwithawide
rangeofpathologiessuchaspoorgeneralization[29],losslandscapesharpness[78],andfinallyplasticityloss[78].
Featureregularization(Section5.4)mitigatesthedownstreameffectsofregressionlosses,whileSection5.7covers
categoricallossfunctionsindetail.
4.5 ParameterNormGrowth
Lyleetal.[78]foundthatparameternormgrowthisacommonpathologyofnetworksthathavelostplasticityand
isassociatedwithreducedtaskperformance.Inthefollowing,wepresentfourpossiblemechanismstoexplainthis
effect.First,Lyleetal.[78]linkgrowingparameternormsandthesharpnessoftheoptimizationlandscape:Asthe
normsoftheparametersgrow,sodoesthemaximumeigenvalueoftheHessian.Thisconnectstotheworksdescribed
inSection4.9,hypothesizingthatcurvaturemayexplainplasticityloss.Second,thesameauthorsalsohypothesize
thatlargeparameternormsmayaffectnonlinearitieswithinthenetwork,suchasactivationfunctionsorsoftmax
headssaturating.TheeffectsofsaturatedunitsaredescribedindetailinSection4.7,butamongthemaregradient
propagationissuesandalossineffectivenetworkcapacity,bothofwhichareassociatedwithplasticityloss.Third,it
hasbeenfoundthatgrowingparameternormsmayleadtogradientswithsparseand/orcollineargradientcovariance
matrices.Asaresult,updatesmayover-generalizeorunder-generalizeinthesamplespace.Inanextremecase,an
over-generalizingnetworkmaylearnadegeneratefunctionthatassignssimilaroutputstoallinputs.Ontheotherhand,
anunder-generalizingnetworkcanonlymemorizetasklabels[78].Bothstatesarelinkedtoplasticityloss.Fourth,
arecentstudyfindsthatlargeparameternormsaffecttheeffectivelearningrateofanetwork.Inparticular,asthe
parameternormsofanetworkgrow,sodoesthenormofitsgradient,leadingtoinstabilityandpotentialplasticityloss
duringtraining[77].Theimpliciteffectofparameternormsonthelearningratecanbemitigatedwithatechnique
calledNormalize-and-Project,whichwediscussinSection5.12.OtherremediesarecoveredinSections5.3,5.4,5.7
and5.8.
4.6 FeatureRankCollapse
Theeffectiverankisameasurecommonlyusedtoassessthequalityoftherepresentationlearnedbyaneuralnetwork
[54,65,77].Tobuildanintuitionofwhyitmatters,notethatanRLagent’svaluefunctioniscommonlycomputed
as𝑉(𝑠) =⟨𝜙(𝑠),W⟩,i.e.,astheinnerproductofnon-linearfeaturesofthestateandweightsW.Nowsupposethat
𝜙(𝑠) ∈R𝑑 islowrank:Thisimpliesthatthenetwork’sfeatureslieinalower-dimensionalsubspaceofR𝑑,potentially
mappingdissimilarstatestosimilarfeaturevectors,whichinturnmakesithardertolearndistinctvaluesforthese
dissimilarstates[82].Forafull-rank𝜙(𝑠),thenetworkmapsdifferentstatestomoredissimilarfeaturevectorsby
utilizingalldirectionsofR𝑑,facilitatinglearningofdistinctvaluesfordifferentstates.Kumaretal.[65]definethe
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 11
effectiverankastheminimum𝑘 suchthatarank-𝑘 approximationofthefeaturematrixexplainsatleasta(1−𝛿)
fractionofitstotalvariance:
Definition4.1(EffectiveRank[65]). Let𝜙:X→R𝑑 beafeaturemappingand𝜙(X) ∈R𝑛×𝑑 beafeaturematrix,e.g.,
theembeddingsofaneuralnetworkforacollectionofsamplesX.Let𝛿 ∈ [0,1]and𝜎 1≥···≥𝜎 𝑑 ≥0bethesingular
valuesof𝜙(X)indecreasingorder.Theeffectiverankisdefinedas:srank 𝛿(𝜙(X))=min (cid:26) 𝑘 : (cid:205)
(cid:205)𝑑
𝑘 𝑖
𝑖
=
=
1
1
𝜎
𝜎
𝑖
𝑖
(
(
𝜙
𝜙
(
(
X
X
)
)
)
)
≥1−𝛿 (cid:27) .
Multipleworksobserveacorrelationbetweenanagent’sperformancedegradationanditsrepresentationbecoming
low-rank.Thisphenomenonisdubbed"rankcollapse"andhasbeenobservedbothinonline[48,65,75]andoffline[45,65]
RL.Kumaretal.[65]establishaconnectionbetweentheeffectiverankofanagent’srepresentationanditsabilityto
learn:Adecreaseintherepresentation’srankleadstoincreasedTDerror.Intheoreticalandempiricalanalysis,Kumar
etal.[65]showthatadropinrankisassociatedwiththelargestsingularvaluesoftherepresentationoutgrowing
thesmallerones,mostlikelycausedbybootstrappinginvalue-baseddeepRL.Thiseffectmaybeexacerbatedin
sparse-rewardenvironmentssuchasMontezuma’srevengeonAtari[79].Gülçehreetal.[45]presentathorough
empiricalstudyandfindthattheassociationbetweeneffectiverankandagentperformanceisnotasstraightforwardas
previouslyassumedinofflineRL.Inparticular,itdependsonpotentiallyconfoundinghyperparameterandarchitecture
choices,suchasthelearningrateandtheactivationfunction.However,theyshowthatthecollapseoftheeffective
ranktoaverysmallvalueisreliableandenablestheidentificationofunderfittingagentswithsuboptimalperformance
attheendoftraining.
Thephenomenonofrankcollapseiscloselytiedtootherphenomenarelatedtothelossofplasticity.InofflineRL,
thereisastrongcorrelationbetweentheeffectiverankandthenumberofdeadunitsintheagent’snetwork[45].
Similarly,resettingdeadordormantneuronsincreasesfeaturerankattheendofonlineRLtraining[107].Currently,
theexactcausalrelationshipbetweendeadneuronsandrankcollapseremainsunclear.Strategiestomitigatetheeffect
ofrankcollapsecanbefoundinSections5.3,5.5,5.6and5.8.
4.7 SaturatedandDormantNeurons
Saturated[16,78]ordormant[107]unitsareoneofthemostprominentpathologiesassociatedwithplasticitylossand
reducedagentperformance.Theyareanobviousandobjectivelymeasurablesignindicatingthatthenetworkcannot
utilizeitsfullcapacity.Therefore,itiseasytorelatethemtoreducednetworkexpressivityandslowlearning[107].
However,itisunclearwhetherdormantneuronsareamaindriverofplasticitylossorjustapathologyassociatedwith
networksthathavelosttheirplasticity.Forexample,Sokaretal.[107]discusstargetnon-stationarityascontributingto
anincreaseindormantneuronsthroughouttraining.OtheraspectsofmoderndeepRLalgorithmsmightalsoexacerbate
thephenomenon,suchastrainingwithhighreplayratios[26,103].
Howcanunitswithreducedcapacitybeformallydefined?Theliteratureprovidesaplethoraofoptionstoachieve
this,whichwecategorizeintotwogroups:Saturatedunits,forwhichashiftinthepre-activationdistributionreduces
theneuron’scapacitytoproducemeaningfullydifferentoutputsgiveninputsfromitsinputdistribution,whichoften
coincideswithvanishinggradients.Forexample,thiscouldbeaReLUneuronwhereallinputsarepositiveornegative,
renderingitinactive(“dead”)[81]orlinear[78],respectively.Dormantunits[107]areinsteadcharacterizedbylow
post-nonlinearityactivations.Whenconsideringatanhunit,onecaneasilyseehowthesecategoriesdiffer:Forlarge
pre-activations,theunit’soutputwillbeclosetooneforallinputs.Importantly,theoutputwillbeclosetoone(i.e.,
showsmallnumericaldifferences),evenconsideringsignificantdifferencesinthepre-activation.Ontheotherhand,
suchasaturatedtanhunitisclearlynotdormantbecauseitspost-nonlinearityactivationishigh.
Preprint

| 12  |     |     | Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek |     |     |     |
| --- | --- | --- | ----------------------------------------------------- | --- | --- | --- |
SaturatedNeuronshavefirstbeendiscussedinBjorcketal.[16]inthecontextoftanhactivationsinpixel-based
continuouscontrol.However,nocommongeneraldefinitionofsaturatedneuronshasemergedyet.Theauthorstooka
closerlookatrunsofthethen-state-of-the-artagentDrQ-v2[119]andobservedthatmostofthemexhibitedsaturated
tanhpolicies,withrunsfailingtolearnandnotbeingabletomoveoutofthisregime3.Thispushesactionstothe
boundariesofthe[−1,1]actionintervaltypicallyusedincontinuouscontrol.When|tanh(𝑔 𝜃(x))|≈1,thederivative
1−tanh2(𝑔 𝜃(x))≈0,causingvanishinggradients.Interestingly,theirproposedsolutiontonormalizethefeaturesof
thepenultimatelayerincreasesperformancewhenappliednotonlytotheactorbutalsotothecritic[16],highlighting
thefactthatboundedactivationsmaybejustasimportanttopreventcriticdivergence[13].
Morerecently,Lyleetal.[78]partitionnon-stationarylearningproblemsintoanerasingorunlearningphaseand
adisentanglementphase,findingthatthefirstcausesaformofsaturationinReLUunits.Theselinearizedunitsare
characterizedbytheirpre-activationdistribution,whichhasonlypositivesupport.Tobemoreprecise,theunlearning
phaseafterataskshiftcausesadistributionshiftintheneuron’spre-activationdistributionthroughgradientsthat
eitherincreaseordecreasethepreactivationvaluesforalltrainingsamples.Ifallpre-activationsforaneuronarenow
positive,theunitbecomeslinearized,removingitsnonlinearcomponent.Ifaneuron’spre-activationsarenegativefor
thetrainingdataset,itmovesintothedeadneuronregime.Bothoftheaforementionedpathologiesreducethenetwork’s
expressivecapacity.Asaremedy,theauthorsproposetoapplyLayerNorm[7]beforeaunit’snonlinearity[78]to
ensure(approximately)zero-meanpre-activations.
DormantNeuronshavebeenintroducedbySokaretal.[107]asameasureforthereducedexpressivityofaneural
network.Inexperiments,ithasbeenshownthatdormantneuronsareassociatedwithperformanceplateausand
reducedperformanceofDQNagents[85]trainedonvariousAtarigames.Todeterminethelevelofdormancy,onehas
tofirstcalculatenormalizedactivationscores𝑠𝑙 foreachneuron𝑖inallnon-finallayers𝑙 [107],i.e.,
𝑖
(cid:2) |ℎ𝑙 (cid:3)
|     |     | E             | x∈D (x)|      |         |     |      |
| --- | --- | ------------- | ------------- | ------- | --- | ---- |
|     |     | 𝑠𝑙 =          | 𝑖             | .       |     | (10) |
|     |     | 𝑖 1 (cid:205) | E (cid:2) |ℎ𝑙 | (cid:3) |     |      |
|     |     | 𝑘∈[𝐻𝑙]        | x∈D           | (x)|    |     |      |
|     |     | 𝐻 𝑙           |               | 𝑘       |     |      |
Herex∈Daresamplesdrawnfromaninputdistribution,e.g.,thereplaybufferinoff-policydeepRL,ℎ𝑙(x)denotes
𝑖
thepost-nonlinearityactivationofaneuroninlayer𝑙,and𝐻𝑙 thenumberofneuronsinlayer𝑙.
|                                     |     | IfthescoreinEquation(10)isbelowathreshold𝜏,i.e.,𝑠𝑙 |     |     |     | ≤𝜏,thenneuron𝑖 |
| ----------------------------------- | --- | -------------------------------------------------- | --- | --- | --- | -------------- |
| Definition4.2(NeuronDormancy[107]). |     |                                                    |     |     | 𝑖   |                |
inlayer𝑙is𝜏-dormant.Denoting𝐻 𝑙 asthenumberofdormantneuronsperlayer,and𝑁𝑙 asthetotalnumberofneurons
𝜏
|                            |                  | 𝑙/𝑁𝑙ofalllayersexceptthefinallayer,𝛽 |     |     | =(cid:205) 𝑙/(cid:205) | 𝑁𝑙[107,117]. |
| -------------------------- | ---------------- | ------------------------------------ | --- | --- | ---------------------- | ------------ |
| perlayer,thedormancyratio𝛽 | 𝜏 isthefraction𝐻 |                                      |     |     | 𝜏 𝐻                    |              |
|                            |                  | 𝜏                                    |     |     | 𝑙∈𝜃 𝜏                  | 𝑙∈𝜃          |
Anagentexhibitsthedormantneuronphenomenonif𝛽 increasesoverthecourseofthetraining.
𝜏
Theabovedefinitionisnottheonlysensiblewaytodefineameasureforneuronswithreducedactivity,butitis
currentlywidelyusedintheliterature[80,93,94,107,117]duetoitssimplicityandintuitiveunderstanding.Dohare
etal.[24]defineamorecomplexmeasureofneuronutilitybasedonaproductbetweenthemagnitudesofaunit’s
summedweightsanditsactivations.AmorestraightforwardoptionforReLUnetworksistosimplycountthenumber
ofzeroactivations[1,30].
Tosummarize:Whiletherearedifferentoptionsfordefininginactiveneurons[24,30,107],alloftheworkscited
aboveagreethattheyareasymptomofreducedexpressivitycausedbysomeformofnon-stationarity[1,80,107].
Wheretheydifferisintheproposedsolutiontoaddressinactiveunits:Sections5.1and5.2discussaplethoraofreset
strategiesaspossibleremedies[24,91,107,117],Section5.6considersactivationfunctionsfornon-stationaryproblems
3DrQ-v2buildsontopofTD3[37],whichisanagentbasedondeterministicpolicygradientsthatusesthetanhfunctiontoclipactionsin[−1,1].
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 13
suchasCReLU[1],andSection5.3examinesparameterregularization[73].Morestrategiestocountertheeffectsof
saturatedordormantneuronsarecoveredinSections5.4,5.10,5.8,5.11,and5.12.
4.8 First-orderOptimizationEffects
Sincedeepnetworksrelyongradient-basedoptimization,gradientpathologiessuchasthewell-knownvanishing
gradientproblem[50]arenaturalcandidatesforplasticityloss.Theymanifestasacollapseinnonzerogradients
andL1gradientnorms4,wherethenetworkcannotadaptdespitehighloss.Gradientsparsity,arelatedphenomenon,
correlateswithsparseReLUactivationsanddeadneuronsinvalue-basedagents[1].Amorenuancednotionofsparsity,
gradientdormancy,adaptstheneurondormancymeasurefromSection4.7byusinggradientL2normsinsteadof
activations.Jietal.[59]findthatgradientdormancyafflictsproprioceptivecontrolagentsinsparse-rewardtasks,
indicatingaconnectionbetweensparsefeedback,degradedlearningability,andrepresentationquality[76].
Explodinggradientsdestabilizetrainingandtypicallycausemoresevereperformancedegradationthanvanishing
gradients.TheyariseinatleastthreedeepRLsettings.First,high-dimensionalcontinuouscontrolenvironments,such
asDMControlDog(38-dimensionalactionspace),generatelargegradientnormsthatcandestabilizetraining[88].
Second,scalingnetworkdepthincontinuouscontrolwithoutregularizationleadstogradientexplosion[15].Third,
off-policyagentssufferfromlargegradientswhencombiningoverestimationbiaswithupdatesonout-of-distribution
(OOD)actions[55].Thisthirdmechanismoperatesasfollows:Bootstrappingwithargmaxinoff-policyalgorithms
selectsoverestimatedOODactionsduetofunctionapproximationerror[112].TheseOODactionsproducelargeTD
errorswithproportionallygrowingcriticgradientsduetotheregressionloss(Section4.4).Largegradientsthenincrease
parameternorms,furtheramplifyingoverestimationandgradientmagnitudesinafeedbackloop.Thiseffectintensifies
whentrainingwithhighreplayratiosoronsmall,fixedbatches[55,91].
Incontrasttovanishingorexplodinggradients,ill-conditionedupdatesareamoresubtleissuerelatedtogradients
inoptimization.Lewandowskietal.[71]examinehownon-stationaritycausedbygrowingparameternormsleads
toacollapseinJacobianranks.Thisreducesthediversityofgradients,withupdatesonlybeingperformedalonga
fewdimensionsinparameterspace.Anothersymptomofill-conditionedgradientsisgradientcollinearity,whichcan
beanalyzedthroughtworelatedmetrics:thegradientcovariancematrix[79]andtheempiricalneuraltangentkernel
(eNTK)[78].Bothexaminerelationshipsbetweengradientsofdifferenttrainingsamples.Thegradientcovariancematrix
usesnormalizeddotproducts(cosinesimilarity)betweenobjectivegradients,whereastheeNTKemploysunnormalized
dotproductsbetweennetworkoutputgradients.Thestructureofthesematricesprovidesdiagnosticinsightsintoboth
optimizationandgeneralization.Positivevaluesbetweensamplepairsindicatethatgradientupdatesgeneralizeacross
thosesamples,whilenegativevaluessuggestinterference.Apronouncedblockstructureinthesematricessignals
asharpandunstablelosslandscape.Mostmatrixentriesbeingeitherpositiveornegativeandofsimilarmagnitude
indicatethatthenetworkhaslearnedadegeneratefunction:updatesonindividualsamplesovergeneralizetotheentire
inputspace,makingitdifficulttodistinguishbetweensamples.Mostoftheavailableremediestoplasticitylosscan
directlymitigatethegradientissuesdescribedabove(cf.Sections5.1,5.3,5.4,5.5,5.6,5.7,5.10,5.8and5.12).
4.9 Second-orderOptimizationEffects
Itiswell-knownfromsupervisedlearningthatflatminimageneralizebetter[36,51].Curvaturealsoappearscentralto
plasticityloss:networksthatloseplasticityoftenshowhighcurvature[68,73,79].Lyleetal.[79]findthatincreased
4Abbasetal.[1]notethatL2gradientnormscanbemisleadingduetodisproportionateweightfromoutliers.
Preprint

14 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
curvature,asmeasuredbythelargesteigenvalueofanetwork’sHessian,makesoptimizationmoredifficultandleadsto
plasticityloss.Inasimilarvein,Lewandowskietal.[73]arguethatacollapseoftheHessian’seffectiverank[65](cf.
Definition4.1)iscausingplasticityloss.Tomeasurecurvature,theyfindthattheempiricalFisherinformationmatrix
outperformsotherapproximations,suchastheGauss-Newtonapproximation,intermsofaccuracy[73].Ifasharp
optimizationlandscapeweretocauseplasticityloss,thenmethodsexplicitlyreducingsharpness,suchastheSAM
optimizer[36],shouldalsomitigateit(cfSection5.10).Leeetal.[68]evaluateSAMinanAtari-100kagentandfindit
veryeffectiveatreducingsharpnessasmeasuredbytheHessian’slargesteigenvalue.However,theirablationstudies
highlightthatresets[91](cf.Section5.1)stilloutperformSAMintermsofcumulativerewardwhenappliedinisolation.
TheperformancegapbetweenresetsandSAMoccursdespitesignificantlyhighercurvaturewhenapplyingtheformer,
indicatingthatsharpnesscannotbethesolemechanismbehindplasticityloss.Leeetal.[68]attributethisperformance
gaptosmoothminimaonlyreducingsensitivitytochangesintheinputdistribution,whereascomplementarymethods
musttackletheorthogonalissueofchangesinthetargetdistribution.Moreover,combinedstrategies(Section5.12)and
parameterregularization(Section5.3)areusefulinmitigatingissueswiththelosslandscape.
4.10 PrimacyBias
Whentrainingnetworksundernon-stationarity,someearlyworkshavehypothesizedthatresidualeffectsofoverfitting
toearlytrainingdatamighthinderlatetrainingprogress.Theearliestworkdescribingthisphenomenonattributesit
tothenetworktryingtore-usesuboptimalfeaturesacquiredearlyduringtraining[56].Theirresultsontoydatasets
havebeenconfirmedindeepRLandsubsequentlynamedthe“Primacybias”[91],borrowingterminologyfroma
psychologicalphenomenonwhereearlyexperiencesdisproportionatelyshapelaterlearning.IndeepRL,thismanifests
asagentsoverfittingtoearlyinteractionsandlosingtheabilitytoupdatetheirnetworkswhenfacedwithnewdata.
Whiletheseearlyfindingsregardingplasticitylosshavebeencompelling,morerecentworkhasmovedawayfromthe
hypothesisofearlyoverfittingtowardsmechanisticandmeasurableexplanationssuchasdeadneurons,parameter
normgrowth,orfeaturerankcollapse.Mitigationstrategiestoprimacybiascomprisenon-targetedweightresetsand
combinedapproaches(cf.Sections5.1,5.4,and5.12).
5 MitigatingLossofPlasticity
Thissectionprovidesanoverviewofmethodsformitigatingplasticityloss.Webeginwithnetworkreinitialization
approachesusinguntargeted(Section5.1)andtargeted(Section5.2)weightresets,thencoverregularizationofweights
(Section5.3)andfeaturerank(Section5.5).Section5.6examinesactivationfunctions,Section5.7discussescategorical
lossreformulation,andSection5.8coversnetworkarchitectures.Wethendiscussdistillation-basedmethods(Section5.9)
andRL-specificoptimizers(Section5.10),followedbymiscellaneoustechniques(Section5.11).Section5.12concludes
withmethodscombiningmultiplemechanisms.Figure2summarizesourtaxonomy.
Preprint

| PlasticityLossinDeepReinforcementLearning:ASurvey |     |     |              |             |          | 15  |
| ------------------------------------------------- | --- | --- | ------------ | ----------- | -------- | --- |
|                                                   |     |     | HardResets   | SoftResets  | AutoSoft |     |
|                                                   |     |     | Non-targeted | Weight      | Resets   | (3) |
|                                                   |     |     | CBP          | ReDo        |          |     |
|                                                   |     |     | UPGD         | Plast. Inj. |          |     |
|                                                   |     |     | Targeted     | Weight      | Resets   | (4) |
|                                                   |     |     | L2Reg        | L2Init      | 2-Wass   |     |
Saturated&Dormant
|     |     |     | SpecNorm | SpecReg | WeightClip |     |
| --- | --- | --- | -------- | ------- | ---------- | --- |
18
|     | Neurons |     | Parseval  |                |     |     |
| --- | ------- | --- | --------- | -------------- | --- | --- |
|     |         |     | Parameter | Regularization |     | (7) |
FeatureRank
10
|     | Collapse |     |           | p-norm         |     |     |
| --- | -------- | --- | --------- | -------------- | --- | --- |
|     |          |     | LayerNorm |                | OFN |     |
|     |          |     | Feature   | Regularization | (5) |     |
First-Order
|     |     | 24  | DirectSV | InFeR | DR3 |     |
| --- | --- | --- | -------- | ----- | --- | --- |
OptimizationEffects
|     |              |     | BEER    | PFO                 |     |     |
| --- | ------------ | --- | ------- | ------------------- | --- | --- |
|     | Second-Order |     | Feature | Rank Regularization |     | (5) |
5
OptimizationEffects
|     |     |     | CReLU     | PELU     | Hadamard |     |
| --- | --- | --- | --------- | -------- | -------- | --- |
|     |     |     | DeepFour. | Rational |          |     |
Non-stationarity
|               |                | 23  | Activation  | Functions     | (5)       |     |
| ------------- | -------------- | --- | ----------- | ------------- | --------- | --- |
|               |                |     | C-51        | Two-hot       | HL-Gauss  |     |
|               | RegressionLoss | 4   | Categorical | Objective     | Functions | (3) |
|               |                |     | MoE         | BroNet        | SimBa     |     |
| ParameterNorm |                |     | Pruning     | NE            |           |     |
|               |                | 14  | Network     | Architectures | (5)       |     |
Growth
|                 |             |     | ITER         | Hare&Tort. |          |     |
| --------------- | ----------- | --- | ------------ | ---------- | -------- | --- |
| HighReplayRatio |             | 12  | Distillation | (2)        |          |     |
|                 |             |     | OPEN         | SAM        | Adam-Rel |     |
|                 | PrimacyBias |     | MomentRst    |            |          |     |
4
|     |               |     | Optimization | (4)         |       |     |
| --- | ------------- | --- | ------------ | ----------- | ----- | --- |
|     |               |     | DataAug      | Discr. Rep. | AdaQN |     |
|     | Method Types: |     |              |             |       |     |
|     |               |     | InputNorm    | Rew. Norm   |       |     |
Domain-spec
|     | General |     | Other Methods | (3) |     |     |
| --- | ------- | --- | ------------- | --- | --- | --- |
Visualization:
|     |                                   |     | NaP      | BBF      | PLASTIC |     |
| --- | --------------------------------- | --- | -------- | -------- | ------- | --- |
|     |                                   |     | BRO      | Stream-X | AVG     |     |
|     | # Driver/Pathology(size=#methods) |     |          |          |         |     |
|     |                                   |     | Combined | Methods  | (6)     |     |
Edgecolor=Driver/Pathology
Fig.2. Bipartitegraphshowingplasticitylossmitigationmethodsgroupedbycategory.Left:Ninecausessizedbythenumberof
methodsaddressingthem.Right:Methodsgroupedinto12categorieswithindividualmethodsshownwithineachcategorybox.
Edgecolorindicateswhichdriverorpathologyacategoryaddresses.Dotsnexttoeachcategoryboxindicatedrivers/pathologies
addressedbymethodswithinthebox.
Preprint

16 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
5.1 Non-targetedWeightResets
Non-targetedweightresetsperiodicallyreinitializenetworklayerstorestoreplasticityandwereinitiallyproposedto
mitigateearlyoverfitting[91].Theycomeintwovariants:(a)Hardresets,wherenetworklayersarefullyreset,and
(b)softresets,whereaconvexcombinationofcurrentandfreshweightsisused.HardResetsfullyresetnetworkweights
usingtheinitializationdistribution.Empiricalevidenceshowsplasticitylossconcentratesinlaterlayers[11,26,91],
motivatingresetsofthefinallayerswhilepreservingearlierrepresentations.Forshallownetworksinproprioceptive
control,thisstillamountstoresettingtheentirenetwork[26,89,91].Inpixel-baseddomainslikeAtari,convolutional
encodersaretypicallypreservedtoretainthelearnedrepresentation[26,91,103].SoftResets[5],a.k.a.Shrinkand
Perturb(S&P),blendcurrentweights𝜃 withfreshlyinitializedparameters𝜓 fromtheinitialweightdistribution[26]:
old
𝜃
new
=𝛼𝜃 old+(1−𝛼)𝜓, 𝜓 ∼initializer.When𝛼 iswell-tuned,S&Prestoresplasticitywhileretainingtask-relevant
knowledge.When𝛼 istoohigh,plasticitymightnotbesufficientlyrestored;when𝛼 istoolow,theresetcanerasethe
learnedknowledge(catastrophicforgetting).
Manyagentsusesomeformofresettingtoaddressplasticityloss.SR-SPR[26]appliessoftresetstotheencoderwith
𝛼 ≈0.8andhardresetstothehead,enablingtrainingwithreplayratiosupto16onAtari-100k.BBF[103]usesthesame
resetstrategyalongsidedeeperresidualnetworks,settingthecurrentstate-of-the-artformodel-freeRLonAtari-100k.
Severalmethodsavoidmanual𝛼 tuning:DrM[117]andACE[59]dynamicallyadjustresetstrengthbasedonplasticity
metrics.DrMusesthedormancyratioasaplasticitymeasure,whileACEusesgradientdormancy(seeSections4.7
and4.8).Galashovetal.[38]takeaBayesianviewonplasticitylossandmodelthedriftoftheoptimalparametersdueto
non-stationaritywithanOrnstein-Uhlenbeckprocess,assumingaGaussianpriorandposteriorfortheweights.When
theirdriftmodeldetectsparameterdriftwithhighprobability,thealgorithmadjuststhenetwork’scurrentweights
(posterior)closertotheinitializationweights(prior),enablingfasterlearning.Conceptually,thisAutomaticSoft
ParameterResetcanbeunderstoodasawideningoftheconfidenceregionuntiltheoptimalparameters𝜃
𝑡
∗forthe
newtaskarecontainedinitwithhighprobability[38],removingthe𝛼 hyperparameterentirely.
Comparinghardandsoftresets,itstandsoutthathardresetsareprimarilyviableforoff-policyalgorithmswith
replaybuffers,whichserveasaformof"memory"thatenablestherapidrecoveryofdiscardedknowledge[26,91].
Withoutabuffer,hardresetsriskcatastrophicforgetting,thoughon-policyusemaybefeasiblewithsufficientlylowreset
frequencies[60].S&Pwithwell-tuned𝛼avoidsforgettingandworkswellinon-policysettings[60].Additionally,S&P
reducesdeadneurons,mitigatesvanishinggradients,andcontrolsweightnormgrowth[30].Additionally,resetsmay
offerexplorationbenefitsthatareorthogonaltoplasticity.Xuetal.[117]hypothesizethatS&Pimprovesexploration
byacceleratingpolicychange[100].Hussingetal.[55]observesimilarexplorationbenefitsarisingfromresetsthat
shiftwhichactionstheQ-functionover-orunderestimates.Thissuggeststhatresetsmayenableaformofoptimistic
exploration.Insummary,hardresetsoffersimplicityandstrongrestorationofplasticityinoff-policysettings,while
softresetsprovidefinercontrolandbroaderapplicabilityatthecostofincreasedhyperparametersensitivity.
5.2 TargetedWeightResets
Insteadofarbitrarilyresettingnetworkweights,algorithmswithtargetedresetstrackameasureofutilityforeach
neuronorparameterandperformresetsaccordingly[24,30,107].Thisallowsresettingonlythepartsofanetworklikely
affectedbyplasticityloss,atthecostofadditionalcomputationalandmemoryoverhead.Inthissection,weexaminefour
approachesthattradecomputationalcostforprecisioninidentifyingneuronstoreset.Allfourmethodssubstantially
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 17
outperformnon-targetedresetsontaskswhereplasticitylossissevere.However,theirrelativeeffectivenessvaries
acrossbenchmarksandagentarchitectures.
ContinualBackpropagation[24]tracksaheuristicutilitymeasureforeachneuronthatisupdatedafterevery
gradientstep.Thealgorithmresetstheleastuseful𝑥%ofneuronsineachlayerbyresamplingincomingweightsfrom
theinitializationdistributionandsettingoutgoingweightstozero.Italsoresetstheoptimizer’smomentestimates
andmaintainsacountertopreventrepeatedlyresettingthesameneurons.WhileCBPshowspromisingresultson
toyproblemsandproprioceptiveRLenvironments,trackingmultiplemetricsperneuronandperformingupdatesat
everygradientstepmakesitcomputationallyexpensiveandmemory-intensive.ReDo[107]reducesoverheadbyonly
checkingevery𝑘timestepswhetheraneuron’sper-layernormalizedactivationsfallbelowathreshold.Neuronsbelow
thisthresholdareconsidereddormantandresetusingthesamestrategyasinContinualBackpropagation.OnAtari,
ReDosubstantiallyimprovesDQNandDrQperformance,particularlyingameswheredormantneuronsareknownto
occur.ImprovementsarelesspronouncedforSACagentsonproprioceptivecontinuouscontroltasksduetodifferent
dormancydynamicscomparedtopixel-basedenvironments[59].UPGD[30]combinestargetedresetswithnoisy
gradientdescentbyscalingthelearningratewithameasureofparameterutility.Parameterswithhighutilityremain
largelyunchanged,whileunimportantparametersreceivestrongerSGDupdatesandareperturbedwithGaussian
noise.Theutilityapproximatesthechangeinlossifaparticularparameterweresettozero,estimatedviaafirst-order
Taylorexpansiontoavoidexpensiveforwardpasses.Thisapproachcanbeviewedasasoft,utility-weightedresetthat
extendsnaturallytomomentum-basedoptimizerslikeAdam.
Unlikethepreviousthreemethodsthatexplicitlymeasureneuronorparameterutility,PlasticityInjection[90]
takesadifferentapproachbyresettingthenetwork’sheadinawaythatpreservesbothoutputsandtrainability.
Buildingontheobservationthatplasticitylossconcentratesinthelastlayers[26],itdecomposestheQ-functionas
𝑄(s)=ℎ 𝜃(s)+ℎ
𝜃 1
′(s)−ℎ
𝜃 2
′(s),where𝜃aretheoriginalfrozenparameters,𝜃
1
′arefreshlyinitializedtrainableparameters,
and𝜃′ isafrozencopyof𝜃′.Thisconstructionensuresthatpredictionsremainunchangedimmediatelyafterthe
2 1
injection,whilethefreshparameters𝜃′ restoretheagent’slearningcapacity.Becauseplasticityinjectionperformsa
1
targetedresetofthenetwork’sheadwithoutmeasuringindividualneuronutilities,itoccupiesamiddlegroundbetween
targetedandnon-targetedresets.Thisdualnaturealsomakesitusefulasadiagnostictool:ifanagent’sperformance
improvessubstantiallyafterinjection,thisconfirmsthatplasticitylosswashinderinglearning[90].
5.3 ParameterRegularization
Regularizingparameternormswasoriginallydevelopedtocombatoverfittinginlinearregression[87].Incontrast,
avoidingplasticitylossfocusesnotonsimplifyingthemodelbutonpreservingitsabilitytolearn.Tothisend,parameter
regularizationhelpsretainpropertiesofinitialweightsknowntosupportrapidadaptation,suchassmallparameter
magnitudes,therankoflearnedrepresentations,orfavorableHessianconditioning.
Small parameter norms may aid training by inducing a smoother optimization landscape via smaller gradient
norms[78],makingparameterregularizationanaturalavenueformitigatingplasticityloss.Afirstfamilyofmethods
regularizesweightstowardtheirinitialconfiguration.Themostprominentapproach,L2Regularization(orweight
decay), adds the squared L2 norm of all weights to the loss: 𝐿 L2reg(𝜃) = 𝐿(𝜃) +𝜆(cid:205)
𝑙
𝑛
=1
∥W𝑙 −0∥2
2
, where 𝐿(𝜃) is
the original objective, W𝑙 the weights in layer𝑙, and 𝜆 determines regularization strength. While well-tuned L2
regularizationcankeepparametermagnitudessmall,itofteninterfereswithtraininginRL,particularlyforvalue-
basedagents[78].L2Init[25]modifiesL2regularizationbyreplacingtheoriginwiththeinitialweights:𝐿 L2Init(𝜃)=
𝐿(𝜃)+𝜆(cid:205) 𝑙 𝑛 =1 (cid:13) (cid:13)W𝑙 −W𝑙,0 (cid:13) (cid:13) 2 2 .Theintuitionisthatinitialweightsarecapableofquicklyfittingtargets,aidingplasticity
Preprint

18 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
preservation.Unliketargetedresetmethods(Section5.2),L2Initdoesnotexplicitlycalculateneuronutilityscores.
Instead,itimplicitlydeterminestheregularizationstrengthbasedonthegradientmagnitude:weightswithlargeloss
gradientsreceivelessregularization,whileunimportantweightsarepulledtowardtheirinitialvalues.2-Wasserstein
regularization[73]addressesalimitationofL2Init,namelythatinitialvaluescontainnoknowledgeaboutthelearning
problem.Insteadofregularizingindividualweightstowardtheirinitialvalues,Wassersteinregularizationenforces
similaritybetweenthedistributionsofinitialandcurrentweightsusingthesquared2-Wassersteindistance5,yielding
𝐿 2-Wass(𝜃 𝑡 ,𝜃 0)=𝐿(𝜃 𝑡)+W 2 2(𝑝 𝑡 ∥𝑝 0).ThisisequivalenttoL2Initwithparameterssortedbymagnitude,asubtlechange
thatallowslargerdeviationsofindividualweightswhilemaintainingdistributionalsimilarity.
Ratherthanconstrainingindividualparametervalues,asecondfamilyofmethodscontrolsthespectralpropertiesof
weightmatrices.SpectralNormalization(SpectralNorm)[84]divideseachweightmatrixbyitslargestsingular
value:W𝑙 ←W𝑙/𝜎 max(W𝑙).Thismakesanindividualfullyconnectedlayer𝐾-Lipschitz.IndeepRL,SpectralNorm
offerstwokeybenefits:itcurbsexplodinggradientsduringnetworkscaling[15,88]andimplicitlyschedulestheAdam
learningrate[42,77].ItalsooutperformsmethodslikeclippeddoubleQ-learninginmitigatingoverestimationbias
andreducesdormantneuronsmoreeffectivelythansometargetedapproaches,suchasReDO[88,107].Spectral
Regularization[71]takesacomplementaryapproachbypenalizinglargespectralnormsratherthanusinghard
constraintsoneachlayer.Theauthorsobservethattherankoftheparametermatrixcorrelateswithgradientdiversity
(lowrankimplieslowdiversityandlosttrainability).Theypreventrankreductionbyaddingapenaltyterm𝑅 spectral(𝜃 𝑡)=
(cid:205)
𝑙
𝑛
=1
(cid:2) (𝜎 max(W𝑙,𝑡)𝑘 −1)2+∥b𝑙,𝑡∥𝑘(cid:3),where𝑘governshowstronglylargespectralnormsarepenalized.Bothmethods
addressspectralpropertiesbutdifferinmechanism:SpectralNormenforcesahardconstraintthroughnormalization,
whileSpectralRegularizationappliesasoftpenaltyduringoptimization.
Finally,severalmethodsimposeexplicitgeometricconstraintsonparameternormsthroughalternativemechanisms.
WeightClipping[29]enforcesthatweightsremaininapredefinedrange[−𝑏,𝑏]aftereachgradientupdate.Here
𝑏 =𝜅𝑠
𝑙
,where𝜅isascalinghyperparameterand𝑠
𝑙
aretheboundsoftheuniforminitializationdistributionforlayer
𝑙.TheprimaryadvantageofweightclippingoverweightdecayorL2Initisthatitdoesnotbiasweightstowarda
specificpointinparameterspace.Instead,theparameterscanmovefreelywithinbounds.However,itonlyworkswith
uniforminitializations,suchasKaimingUniform.ParsevalRegularization[20]preservesrow-wiseorthogonalityof
orthogonalinitialization,whichoffersthreebenefits:itimplicitlyregularizesallsingularvaluestoone(strongerthan
SpectralNorm’sconstraintonthelargestsingularvalue),itpreventsparameternormgrowth,andorthogonalweight
matricesaredynamicalisometriesthatpreventexplodingorvanishinggradients[19].However,theorthogonality
constraintmaysubstantiallyreducenetworkexpressivitybylimitingitsLipschitzconstant;thiscanbemitigatedby
learnedinputscalingoradditionalscalinglayers[19].
5.4 FeatureRegularization
Itiswell-establishedthatneuralnetworklayersworkbetterwithinputsthatareeitherwithinspecificrangesorfroma
standardNormaldistribution.Wenowconsidernormalizationinthecontextofplasticityloss.
LayerNormalization(LayerNorm)[7]overcomesBatchNorm’s[58]batch-sizedependenceandsupportsrecurrent
architectures.Itnormalizesalayer’spre-activationsa𝑙 usingper-layerstatisticsbeforeapplyingthenonlinearity[77,78,
89].Thetransformationa𝑙 ← √a𝑙−E[a𝑙] ·𝜸+𝜷involveslearnablescale𝜸 andbias𝜷,with𝜖 >0fornumericalstability.
Var[a𝑙]+𝜖
5The2-WassersteindistanceisW
2
2(𝑝𝑡 ∥𝑝0)=(cid:205)
𝑙
𝑛
=1
(cid:205)𝑑
𝑖=1
(cid:16) 𝑤¯
𝑙
𝑖
,𝑡
−𝑤¯
𝑙
𝑖
,0
(cid:17)2 with𝑤¯
𝑙
𝑖
,𝑡
denotingthe𝑖-thlargestparameteroflayer𝑙atstep𝑡.
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 19
IntroducedbyLyleetal.[79]asaremedyforplasticityloss,LayerNormhassinceshownconsistentbenefits[77,78,
88,89].Itreducesgradientcovariance[79]andstabilizespre-activations,mitigatesoverestimationbias[88],reduces
dormantneurons[107],andcurbslargegradients[88].Moreover,LayerNormenhancesstabilityinvalue-basedRL,
akintoboundedactivations[13],bypreventingunitlinearizationthroughastabilizedpre-activationdistribution[78].
IthasalsobeenshowntorevivedeadReLUunitsbyinjectingnon-zerogradientsthroughnormalization[77],aneffect
confirmedintransformers[118].
Infact,studieswithtransformernetworkshaveshownthatthegradientsfromnormalizationstatisticsarethedriving
forcebehindLayerNorm’sbenefits[118]andnotthezero-mean,unit-varianceactivationsthatwerehypothesized[7,77].
Moreover,Lyleetal.[77]demonstratedthatLayerNormintroducesanimplicit,parameter-norm-dependentlearning
rateschedule,whichmaybenecessaryfordeepRLagentstolearncertainbehaviors.
Bjorcketal.[16]introducep-normtonormalizethepenultimatelayer’sfeaturesinactornetworkstoprevent
saturationoftanhactivationsincontinuouscontroltasks.p-normrescalesthepenultimatelayer’sfeatures𝜙(s)via
𝜙 norm(s) =
∥
𝜙
𝜙
(
(
s
s
)
)∥
,followedbyalinearlayerandtanhactivation.ThoughdesignedforDrQ-v2’sactor[119],Bjorck
etal.[16]alsoapplyp-normtothecritic,observingnotablegainsinstabilityandperformancewhenbothnetworksare
regularized.
Lastly,OFNmitigatesQ-valueoverestimationbyprojectingthecritic’sencoderfeaturestotheunitball[55],thereby
decouplingthescaleofQ-valuesfromearly-layerparameternorms.Thispreventsgradientdivergenceandcontrols
parameternormgrowth.Theauthorsdemonstratethatevenunderstrongprimacybias[91](overfittingtoafewearly
samples),OFN-regularizedagentscanmatchtheperformanceofunprimedones.OFNalsocomplementsparameter
resets,helpingcounteractpessimismfromclippeddoubleQ-learning[37]topromotebetterexploration[55].
5.5 FeatureRankRegularization
Featurerankcollapsefrequentlyco-occurswithplasticityloss[24,25,79],thoughthecausalrelationshipremains
unclear.Motivatedbyobservationsthatunder-parameterizedandlow-rankrepresentationscorrelatewithdegraded
performanceinvalue-baseddeepRL,severalalgorithmsexplicitlytargetrankpreservationtomaintainlearningcapacity.
Kumaretal.[65]introduceDirectSingularValueRegularization,whichpenalizesdominantsingularvalues
oftherepresentationmatrixtoencourageamorespread-outdistribution,therebyincreasingrank.However,this
approachishighlysensitivetohyperparametertuningandpronetoproducingcollapsedrepresentations.InFeR[75]
takesadifferentapproach,usingauxiliaryregressiontaskswithfixedrandomtargetstoindirectlyencouragediverse
featurelearningandahighereffectiverank.InFeRhasshownpromiseinpreventingplasticityloss[75]andimproves
representationlearninginsparse-rewardenvironments[76].Incontrast,DR3[66]regularizestherepresentation
directlybypenalizinglargedotproductsbetweenrepresentationsofconsecutivestates,effectivelypreventingfeature
co-adaptation.Althoughnotdesignedtoexplicitlypreserverank,DR3empiricallypreventscollapseandimproves
performance.Buildingoninsightsaboutfeaturesimilarity,Heetal.[48]adaptivelyregularizerankbasedonanupper
boundofthecosinesimilaritybetweenconsecutivestaterepresentations.Unlikethepreviouslymentionedalgorithms,
theirmethodBEERaimstoadjusttherankaccordingtotaskcomplexity,leadingtopotentiallybetterperformanceand
moreaccuratevalueestimatescomparedtomethodsthatsimplymaximizerank.Unlikethemethodsabove,whichtarget
off-policysettings,PFO[86]addressesplasticitylossintheon-policysettingbyanalyzingtheconnectionbetween
policyupdates,representationrank,andtrust-regioncollapseinPPO[102].PFOextendsPPO’strust-regionconceptto
featurespacebyapplyinganL2penaltytopreventthepre-activationfeaturesofthecurrentpolicyfromdriftingtoofar
fromthoseofthedata-collectingpolicy.
Preprint

20 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Thepreciserelationshipbetweeneffectiverank,featurerankcollapse,andplasticitylossremainstobeinvestigated.
Whileadropineffectiverankappearstobeacommonpathologyofagentsthatstruggletolearn[25,45,65],itisstill
debatedwhethermaximizingrankisalwaysbeneficial,withsomemethodslikeBEERsuggestinganadaptiveapproach
isbetter[48].Gülçehreetal.[45]’sstudyinofflineRLindicatesthatnetworkarchitectureandtraininghyperparameters,
suchasactivationfunctionsandlearningrates,playasignificantroleinrankcollapse.Furthermore,theyobservea
strongcorrelationbetweenthenumberofdeadunitsandeffectiverank,althoughwithoutestablishingastrongcausal
direction[45].Insummary,whilefeaturerankcollapseisstronglyassociatedwiththelossoflearningability,itsexact
roleandwhetheritisadriverorasymptomofplasticitylossarestillsubjectsofongoingresearch.
5.6 ActivationFunctions
Certainactivationfunctionsaremorepronetocausingdeadordormantneuronsthanothers[81,107],makingthema
naturalavenueforimprovingnetworkplasticity.Inthissection,wereviewvariousactivationfunctionsproposedin
theliteraturetoaddressplasticityloss,includingtwospecificallydesignedtopreserveit(DeepFourierFeaturesand
AdaptiveRationalActivations).Forclarity,wedefineallfunctionselement-wiseusingascalarinput𝑥 ∈R.
Whileoriginallyproposedforimageclassification[104],Abbasetal.[1]applyCReLUtodeepRL,whereCReLU(𝑥)=
(cid:104) (cid:105)
ReLU(𝑥),ReLU(−𝑥) concatenatestheReLUoutputwithitsnegation.Theyreportthreemainbenefits:improved
adaptabilitylateintrainingandaftertaskswitches,bettergradientflowwithreducedcollapse,andfewerdeadneurons.
ThislastpropertyholdssinceCReLU(𝑥)=0ifandonlyif𝑥 =0.Incontrast,ReLUoutputszeroforall𝑥 ≤0.
ParameterizedExponentialLinearUnits(PELU)havebeenshowntooutperformbothReLUandCReLUon
Atari,particularlyinenvironmentswithstarkinputdistributionshifts[23].PELUgeneralizestheELUactivation[21]by
introducinglearnableparameters[41],allowingtheactivationslopetoadaptdynamically.Usinglearnableparameters
𝛼 and𝛽,itisdefinedasPELU(𝑥)= 𝛼ℎfor𝑥 ≥0andPELU(𝑥)=𝛼 (cid:16) 𝑒 ℎ 𝛽 −1 (cid:17) for𝑥 <0.
𝛽
Kooi et al. [64] introduce Hadamard Representations by computing the Hadamard product of two parallel
hiddenlayerswithtanhactivationsbeforetheQ-function.WhilenaivetanhactivationsunderperformReLUinAtari
agents,HadamardrepresentationsoutperformReLUwhilepreservingeffectiverank[65]andpreventingdormant
neurons[64,107].
Lewandowskietal.[72]showthatlinearfunctionapproximatorsavoidlossofplasticity,extendingthisfinding
theoreticallytodeepdiagonallinearnetworksandempiricallytogeneraldeeplinearnetworks.Tobalancetheplasticity
oflinearmodelswiththeexpressivityofnonlinearones,theyproposeDeepFourierFeaturesusingFourier(𝑥) =
(cid:104) (cid:105)
sin(𝑥),cos(𝑥) astheactivationfunctionineverylayer.Thisconcatenationensureshalftheunitsperlayerare
approximatelylinear,allowingnetworkswithdeepFourierfeaturestoapproximatelyembedadeeplinearnetwork
withboundederror(Corollary1[72]).
AdaptiveRationalActivationsaredefinedasR(𝑥)= P(𝑥) =
(cid:205)𝑚
𝑗=0
𝑎𝑗𝑥𝑗
,whereP(𝑥)andQ(𝑥)aretwopolynomials
with𝑚+1and𝑛learnableparameters.Theyoffertwok
Q
e
(
y
𝑥)
adva
1+
n
(cid:205)
ta
𝑛 𝑘 g=1
e
𝑏
s
𝑘
:
𝑥
a
𝑘
daptingtoshiftsininputdistributionand
approximatingresidualconnections.Inpractice,thedenominatorusesanabsolutesumand𝑚=𝑛+1[23]6.
Insummary,itappearsthatactivationfunctionscanhelpmitigateplasticitylossbyreducingthenumberofdead
unitsandenhancinggradientflow.However,multipleexperimentshaveshownthatplasticitylossstilloccurswith
differentactivationfunctions[24,107],indicatingthatwhilespecificchoicesmayalleviatesymptoms,theactivation
functionitselfisnottherootcause.
6Delfosseetal.[23]use𝑚=5and𝑛=4throughouttheirpaper.
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 21
5.7 CategoricalObjectiveFunction
Fig.3. VisualizationofcategoricallossesfordeepRL.Thetwo-hotrepresentation[101]proportionallyassignsprobabilitymass
tothetwoneighboringbinsofascalartarget𝑦.HL-Gauss[57]constructsaGaussianwithfixedstandarddeviationandintegrates
overeachbintoobtainthecorrespondingprobabilitymass.DistributionalRLalgorithmssuchasC51[8]modelthefullreturn
distribution.DetaileddescriptionsofthesemethodsareinSection5.7.FiguretakenfromFarebrotheretal.[34].
Itiscommonknowledgeamongdeeplearningpractitionersthatscalingnetworksizesiseasierforclassification
comparedtoarbitraryregressiontasks7[34,57].Evenwhenregressionistheactualtask,reformulatingthelearning
problemusingacross-entropylossisoftenbeneficial[34,57].AsexplainedinSections4.4and4.5,regressiongradients
areproportionaltotheloss,whichinturnmayleadtoparameternormgrowthandotherpathologies.Oneremedyisto
reformulatevalueestimationasclassification:binaboundedrewardrange(usuallyclippedbetween(−10,10)[8])into
discretecategoriesandapplyacross-entropyloss.ThethreemostwidelyusedcategoricallossmethodsareC-51[8],
two-hotrepresentations[101],andHL-Gauss[34].Theirdifferenceslieinhowtheyprojectascalartargetvalueonto
thecategoricalbins,visualizedinFigure3.
C-51[8]approximatesthefullreturndistributionbydirectlyprojectingitonto51categoricalbins,emphasizing
expressivityanddistributionalmodeling.Two-hotrepresentationsofferasimplerapproach,assigningprobability
massonlytothetwonearestbins,whichsoftenstargetsandreducesplasticityloss[78,101].HL-Gaussgeneralizes
thisfurtherbyfirstsmoothingthetargetdistributionwithGaussiannoisebeforespreadingtheprobabilitymass
acrossmultiplebins[57].Thisresultsinaricherrepresentationthatbettercapturestheordinalstructureofregression
problems[34].Allthreemethodsuseacross-entropylossandmitigateplasticityloss.However,theyprovidedifferent
trade-offsonthespectrumofexpressiveness,simplicity,andtrainingrobustness.
C-51’sperformancegainsareoftenattributedtoenablinguncertaintyquantification.However,[34]claimthatthe
categoricalloss,notdistributionalmodeling,isthemaindriverofimprovedsampleefficiency.Two-hotrepresentations
offeralightweightalternativetodistributionalalgorithmslikeC-51,buttheirsimplicitycancomeatthecostoftraining
stability[78]. HL-Gaussenables moreexpressivetarget distributionsand improvedperformance acrosstasks. Its
advantageslikelystemfromtwofactors.First,distributingprobabilitymassactslikelabelsmoothing,whichhelps
reduceoverfitting.Second,HL-Gaussleveragestheordinalnatureofregressiontargets,allowingforbettergeneralization
acrossvalueranges[34].However,itremainsunclearwhichcategoricalprojectionworksbestforaparticulardeepRL
algorithm.Forinstance,Farebrotheretal.[34]showthatHL-Gaussperformswellwithdiscrete-controlalgorithms
7Imagereconstructionusingper-pixelregressionsidestepscommonregressionissuessuchaslargeerrorsandunstablegradientsbyexploitingthefact
thatpixelvaluesarebounded.Thisenablestheuseofnormalizedobjectives,whichdonotworkforunboundedregressiontargetscommonindeepRL.
Preprint

22 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
suchasDQNandCQL.Incontrast,Naumanetal.[89]findthatImplicitQuantileNetworks[9]outperformHL-Gauss
withcontinuous-controlSACagents.
5.8 NetworkArchitectures
NetworkarchitecturesindeepRLaretypicallymuchsmallerthanthoseusedinsupervisedlearning,withagentsoften
relyingoncompactMLPs[46]orDQN-styleCNNs[26,85].Whilelargerandwidernetworkscanimproverobustness
toplasticityloss,optimizationchallengeslimittheirsize[34,89,103].RecenteffortstoscaleupdeepRLmodelshave
focusedonadoptingresidualarchitecturesandregularizationtechniques,suchasLayerNorm,SpectralNorm,orL2
regularization[70,89,103].
WhiletheprimarygoalofbespokenetworkarchitecturesfordeepRLisoftenparameterscaling[70,94],these
modificationsalsofrequentlycontributetomitigatingplasticityloss.Inactor-criticmethods,improvedarchitectures
aremainlyappliedtothecritic,whereplasticitylossisconcentrated[80,88].Consequently,networkarchitecturesthat
enablestabletrainingwithahighernumberofparametersofteninherentlyimproveplasticity.Manyofthecomponents
utilizedbythemethodsbelowwereoriginallydesignedforsupervisedlearning.Withtherightmodifications,they
havebeensuccessfullyadaptedtodeepRL.
Severalarchitecturalapproachesfocusonstructuredsparsityandefficientparameterutilizationthroughstatic
architecturesthatdonotadaptduringtraining.MixtureofExperts(MoEs)[95]introduceagatingmechanismthat
routes inputs to specialized “expert” networks, allowing for parameter scaling without the proportional increase
in computational cost incurred by wider feedforward layers. BroNet [89] and SimBa [70] utilize stacked residual
blocks[47]inthecriticofSACagentstoefficientlyscaleparameterswhilemaintainingstabletraining.Bothare
inspiredbytransformerarchitecturesandsharecommonbuildingblocks,suchasLayerNormandresidualconnections.
ComparedtoBroNet,SimBautilizesaninputnormalizationlayercalledRSNorm,whichhelpsinavoidingoverfitting
whenscalingupthenetwork[70].BothBroNetandSimBacanbeusedasreplacementsforstandardcriticarchitectures
inagentslikeSAC.UnlikeBRO,SimBadoesnotnecessitatefurtheralgorithmicmodificationslikeusingadistributional
lossandweightdecay[70,89].MoEs,SimBa,andBroNetallenableparameterscalingandhelpmitigateplasticityloss.
MoEsachievesthisbyselectivelyactivatingpartsofthenetworkinthepenultimatelayer,whichcontainsmostofthe
parametersofadeepRLagent.BroNetandSimBainsteadrelyonresidualconnectionsandnormalizationtechniquesto
enablestableparameterscalingwithoutoverfittingandtraininginstabilities.
Othermethodsallowfordynamicmanipulationofthenetwork’sstructureduringtraining.NetworkPruning[94]is
basedontheobservationthatnetworksoftenunder-utilizeparameters.Itappliesgradualmagnitudepruningtoremove
theleastimportantconnections,enhancingperformanceandenablingnetworkscalingwhileimprovinggradient
covarianceandotherplasticitymetrics(SeeSection4.8).NeuroplasticExpansion(NE)[74]dynamicallyadjustsnetwork
topologybothbyaddingnewconnectionsbasedongradientnormsandpruningdormantneurons.Thetopology
adjustmentphaseisinterleavedwithaconsolidationphasetopreventcatastrophicforgetting.Incontrasttopruning,
NEdirectlymaintainsplasticitybyaddingnewconnectionswhileaddressingcatastrophicforgettingthroughthe
consolidationphase[74].BothpruningandNEaimtomakenetworkusagemoreefficient,butpruningprimarily
reducesredundantparameters,whileNEactivelyadjuststhenetworktoadapttonewinformation.
5.9 Distillation
Distillationalgorithmsaimtotransferknowledgefromateachernetworktoastudentnetwork,mitigatingnegative
sideeffectsduringtraining[49].ITER[56]periodicallydistillstheactorandcriticnetworksofPPOagentstoaddress
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 23
plasticityloss.Byupdatingthestudentinparallelwiththeteacher’sRLtraining,ITERavoidsrequiringareplaybufferin
on-policyalgorithmslikePPO.Hare&TortoiseNetworks[69]combinedistillationwithperiodicresetsusingadual
architecture:a“hare”networkrapidlylearnsviaSGDwhilea“tortoise”networkslowlyintegratesinformationthrough
anexponentialmovingaverageofthehare’sparameters.Thehareisperiodicallyresettothetortoise’sparameters,
enablingfrequentresetswithoutlosingaccumulatedknowledgeandprovidingamechanismtoescapesuboptimallocal
minimaforthehare.
5.10 Optimization
OptimizationindeepRLdiffersfromsupervisedlearningduetonon-stationarydataandshiftingtargetsthatviolate
i.i.d. assumptions. Value-based RL algorithms perform fixed-point iteration, approximated by stochastic gradient
descent[108],whichcomplicatesoptimization.Whilemomentum-basedoptimizerssuchasAdam[63]workreasonably
wellbyautomaticallyselectingstepsizes,theyoftenrequireadjustments[4,28]likeamuchlargerstabilityparameter
𝜖[53,107]topreventmomentestimatedivergence.ThishasmotivatedRL-specificoptimizers,suchasAdam-Rel[28]
andOPEN[43],whicharepresentedinthissection.
OPEN[43]meta-learnsanoptimizertoaddressdeepRL’schallenges:non-stationarity,plasticityloss,andexploration.
ThegradientupdateusesasmallRNNwithlearnedstochasticity,meta-trainedtooptimizefinalreturn.Byconditioning
onfeatureslikeneurondormancyandnetworkdepth,itbecomesnaturallyrobusttoRL’snon-stationarity.OPEN
usesparameter-spacenoisetoreawakendormantneurons[107]similartoElsayedandMahmood[30],effectively
aidingexplorationandpreventingplasticityloss.ThisexplicitfocusonRLdifficultiesyieldsimprovedperformance
acrossenvironmentscomparedtoothermeta-learningapproaches.Ontheotherhand,Sharpness-AwareMinimization
(SAM)[36]improvesgeneralizationbyseekingflatminima,whichmayenhanceplasticitybyreducinglosslandscape
curvature [68, 79]. Unlike other optimizers, SAM explicitly perturbs gradients to identify low-curvature regions,
requiringtwogradientcomputationsperiteration[36].WhileOPENusesparameternoisetomaintainplasticity,SAM
perturbsgradientstofindflatminima[36].
AseparatelineofworkfocusesonmodifyingoptimizersfordeepRL.Adam-Rel[28]resetsAdam’sinternalstepcount
everytimeanon-stationarityoccurs,enablingrapidadaptationofmomenttermstoshiftsingradientstatistics[28].
Momentresetting[4]isarelatedtechniquethatreinitializesmomentumbuffersateachtargetnetworkupdateto
preventoutdatedmomentsfromcontaminatingupdates.Inoff-policyRL,targetnetworkupdatescanincreasegradient
normsdisproportionatelybetweenfirstandsecondmoments8,potentiallycausingtrainingdivergence[79].Whileboth
methodsaddressthemismatchbetweenstationarityassumptionsandnon-stationaryRLdynamics,momentresettingis
moresevere.Inon-policyRL,itmaydiscardusefuloptimizationinformationthatAdam-Relpreserves[28].
5.11 OtherMethods
Inthissection,wediscussmethodsrelevanttoplasticitylossthatdidnotfitintopreviouscategories.Manyarewell-
knownregularizationtechniques,suchasspecifictypesofrepresentations,input/targetscaling,orhyperparameter
selection.Whiletheywerenotinitiallydesignedtomitigateplasticityloss,theynonethelessaffectit.Forinstance,input
andtargetscalingcanreduceinputortargetnon-stationarity.Bothtechniqueshavebeenaroundforawhile[102]
andmayyieldenvironment-dependentperformancebenefits[3,32,52].Onthehyperparameterfront,AdaQN[115]
automaticallyselectshyperparametersonlinebytraininganensembleofQ-networkswithdifferentconfigurationsand
8PyTorchusesdefaultvaluesof𝛽1=0.9forthefirstmomentand𝛽2=0.999forthesecondmoment[99].
Preprint

24 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
selectingasharedtargetnetworkbasedonrecentlossvalues,enablingadaptationasoptimalhyperparametersshift
acrosstrainingstages[92].
Data Augmentations have driven impressive sample efficiency gains in pixel-based control. Their success is
conventionallyattributedtoimprovedrepresentationlearning[67,119,120].However,Maetal.[80]provideevidence
thatdataaugmentationsactuallymitigateplasticitylossduringcritictrainingbypreventinganearlydropinactive
units.Buildingonthisinsight,theyproposeincreasingthegradientstepsperenvironmentsteponcetheearlystageof
plasticitylosshaspassed.Borrowingfromvector-quantizedgenerativemodels[111],Meyeretal.[83]findthatSparse
Representationsgeneralizebetterandadaptfastertoenvironmentalnon-stationaritieswhentrainingworldmodels.
Theyattributetheseresultstothesparse,binarynatureofone-hotembeddings:one-hotrepresentationssubstantially
outperformquantizedonesdespiteidenticalinformationcontent[83].
5.12 CombinedMethods
Sincetheexactcausesofplasticitylossremainunclearandlikelyinvolvemultipleinteractingfactors[78,79],integrating
differentmitigationstrategiesthattargetspecificsymptomsisasensibleapproach.Consequently,manysuccessful
algorithmsemploymultiplecomplementaryregularizers.ThefirstpopularcombinationisLayerNorm+L2regularization,
introducedbyLyleetal.[79].Subsequently,Naumanetal.[88]examinewell-performingcombinationsforSACagents
andfoundthatResets+L2regularization,aswellasLayerNorm+Resets,workparticularlywell.Inthefollowing,we
willsummarizeparticularlywell-performingcombinationsthathaveachievedstrongresults.
Effectivecombinationsoftenexplicitlyaddressmultiplepotentialdrivers,suchasinputandtargetnon-stationarity,
whilecontrollingpathologieslikegrowingparameternormssimultaneously.Onesuchalgorithm,PLASTIC[68],
combinestheCReLUactivationfunction[1]withsharpness-awareoptimization(SAM)[36],LayerNorm[7],and
resets[91]toachievestrongperformanceonbothAtari-100kandtheDeepMindControlSuite.Anothercombination,
Normalize-and-Project(NaP)[77],pairsLayerNormwithaprojectionstepsimilartoSpectralNorm,whereweightsare
projectedontoaballwithradius𝜌insteadoftheunitball:W𝑙 ←𝜌W𝑙/∥W𝑙∥.ThiscombinationremovesLayerNorm’s
implicitparameter-norm-dependentlearningrateschedule,butpotentiallynecessitatestheintroductionofanexplicit
scheduleinstead.Lyleetal.[77]findthatsimplelineardecayproportionaltoparameternormgrowthsuffices.
Achieving strong performance often requires scaling up network capacity while deploying multiple plasticity-
preservingtechniquessimultaneously.BBF[103]achievesstate-of-the-artmode-freeperformanceonAtari-100kby
employingadeeperResNet-basedarchitecture(IMPALA-CNN[33]).Furthermore,BBFuseshardresetsforthenetwork
headwithsoftresetsfortheencoder,andemploysweightdecaytoenablestabletrainingathighreplayratios.BRO[89]
setthethenstate-of-the-artforproprioceptivecontinuouscontrolbycombiningfullnetworkresetswithLayerNorm
andweightdecay.Additionally,BROincorporatesabespokeresidualnetworkarchitecture,optimisticexploration,and
aquantilenetworkforthecritic,furtherenhancingsampleefficiency.
Lastly,bothAVG[114]andStream-X[31]tacklestreamingRLinsettingswhereagentsprocesstransitionsoneby
onefromasingleenvironment,precludingbatchupdates.Duetothehighvarianceinthisregime,bothmethodsemploy
observationandreward/errornormalization.Notably,scalingrewardvaluesmayreduceplasticitylossbyavoiding
regressiontolargetargets(cf.Section4.4),whichisassociatedwithharmfulparameternormgrowth(cf.Section4.5).
AVGusesp-norm[16]foradditionalregularization,whileStream-Xemploysacustomoptimizer,sparseinitialization,
andLayerNormtomaintainplasticitythroughouttraining.Bothmethodsachieveperformancecompetitivewith
traditionaldeepRLalgorithmsonhigh-dimensionalcontinuousanddiscretecontrolbenchmarks.
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 25
BRO BBF
Hard Resets
3
BroNet
1 Soft Resets
1
SAM L2 Reg
1 2
Combined
Methods
1 SpectralNorm
CReLU 1
4 LayerNorm
1 1 1 NaP
p-norm Input Norm
Reward Norm
PLASTIC
Stream-X
AVG
Component Types: Driver/Pathology:
Saturated&DormantNeurons RegressionLoss
3 Generalregularizer(usagecount)
FeatureRankCollapse ParameterNormGrowth
First-OrderEffects HighReplayRatio
1 Domain-specific
Second-OrderEffects PrimacyBias
Combinedmethod((Sec5.12) Non-stationarity Component→Combined
Fig.4. CombinedplasticitylossmitigationmethodsfromSection5.12.Innerring:Componentmethods,coloredbytype(blue=
generalregularizer,orange=domain-specific),sizedbyusagefrequency.Numberinsidenodeindicateshowmanycombinationsuse
thiscomponent.Outerring:Sixpublishedcombinedmethods.Coloreddotsindicatecausesaddressed(seelegend).Dashedlines
connectcomponentstocombinations.LayerNormismostfrequentlyused(4/6),followedbyHardResets(3/6)andL2Regularization
(2/6),demonstratingthateffectivecombinationsleveragegeneralregularizersacrosscategories.
6 CurrentStateandFutureDirections
Thefieldofplasticitylosshasmadesubstantialempiricalprogressinrecentyears,thoughsignificantgapsinunder-
standingremain.Inthissection,wesynthesizethecurrentstateofknowledgeandidentifythestrengthofevidencefor
particularaspects.
Weknowthatmultipleinterventionsrobustlyimproveperformance[34,42,79,88]:resets[5,91],LayerNorm[7],
SpectralNorm[84],andcategoricallosses[57].IndeepRL,networkssufferingfromplasticitylossshowmultiple
measurable pathologies that correlate with reduced performance: dormant neurons [107], rank collapse [65, 86],
growingparameternorms[71,78],andgradientpathologies[55,59,71].Bothinputandtargetnon-stationarityoccur
ubiquitouslyinthisdomain[68,69,107],thoughquantifyingitsseverityremainschallenging.
Preprint

26 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Despitetheempiricalprogress,welackafundamentalunderstandingofwhytheseinterventionswork.Resetsrestore
learningability[91],butwhethertheyworkbyeliminatingdormantneurons,reducingparameternorms,improving
optimizationdynamics,orsomecombinationremainsunclear.LayerNorm[7]isamongthemosteffectiveregularizers,
yetwecannotdefinitivelystatewhicheffectdrivesitsbenefits:maintainingnormalizedactivations[7,77],inducing
implicitlearningrateschedules[77],orpreventingdeadneuronsthroughnormalizationgradients[118].
Currently,thefieldhasidentifiedcorrelationsbutrarelyestablishedcausation.Figure1presentsplausibleconnections
betweenpotentialfactorscontributingtoplasticityloss,buttheserelationshipsrepresenthypothesesratherthanproven
causallinks.Forexample,targetnon-stationaritycorrelateswithdormantneurons[107],butthisfindingdoesnot
constitutearigorouscausalrelationship.Beyondgapsinunderstanding,thefieldfacesmethodologicalchallengesthat
limitthegeneralizabilityandreproducibilityofresearchonplasticityloss.Inthefollowingsubsections,weexamine
currentmethodologicalissuesthatconstrainprogressandoutlinepriorityresearchdirectionsthatcouldadvanceboth
ourunderstandingandpracticalmitigationofplasticityloss.
6.1 CurrentMethodologicalIssues
ResearchonplasticitylosshastraditionallyfocusedonAtarifordiscretecontrolandtheDeepMindControlSuite(DMC)
forcontinuouscontrol.However,broadeningtheevaluationrevealsthatenvironmentsexhibitdifferentpathologiesat
differentseverities:whileDMC’sDogenvironmentcausesgradientexplosioninSACagents,MetaWorldenvironments
sufferfromgreaterparameternormgrowth[88].Interventioneffectivenessvariesaccordingly:LayerNorm[7]substan-
tiallyimprovesperformanceonDogbystabilizinggradients,yetitisactivelyharmfulwhenappliedonMetaWorld[88].
Similareffectscanbeseenacrossalgorithms:WhileReDohelpsfortheoff-policyalgorithmDQNonAtari[107],itis
outperformedbyotherparameterregularizersfortheon-policyalgorithmPPO[60].Thisvariabilityhighlightsacritical
gap:Wecannotyetpredictwhichenvironmentpropertieswillcausesevereplasticitylossandwhichinterventionswill
proveeffectiveforagiventask.Withoutthispredictivecapability,practitionersmustresorttoexhaustivetrial-and-error
testing.Systematicevaluationacrossdiversebenchmarkscouldidentifymeasurableenvironmentpropertiesthat
predicttheseverityofplasticityloss,movingthefieldfromreactivetoproactivealgorithmdesign.Suchevidence-based
regularizerselectionwouldalsofacilitatetestingforunintendedsideeffectsofpopularmethods.
Thissystematicevaluation,however,dependsonestablishingconsensusonmeasurement.Thefieldcurrentlylacks
agreementonhowtomeasureplasticitylossacrossdifferentsettings,makingitdifficulttocompareinterventionsacross
studies.Researchersemployvariousmetrics,includingneurondormancyratios,effectiverank,andgradientnorms,
butnoneareusedconsistentlyorcomprehensively.Thisinconsistencypreventssystematicmeta-analysisofwhich
algorithmsworkbestunderwhichconditions,obscuringtheabilitytoidentifyuniversalprinciplesunderlyingplasticity
loss.WebelievethatastandardizedevaluationprotocolshouldprioritizethemetricslaidoutinTable3.Notably,we
omitfeaturerankandneurondormancymetrics.Thisisbecausewebelieveneurondormancytobeadownstream
effectofoptimizationissuesthatcanbecapturedbetterbymeasuringgradientnorms[59],andparameternormstobe
agoodproxyindicatorforrankissues[71,86].
6.2 UnderstandingMechanisms(HighestPriority)
Establishingcausalmechanismsbehindplasticitylossrepresentsthefield’smostcriticalgap.Withoutamechanistic
understanding,wedeveloptechniquesthroughtrialanderrorratherthanprincipleddesign.Makingprogressrequires
controlledstudiesthatisolateindividualfactorsandestablishcausalrelationships,ratherthanjustbenchmarkingfinal
performance.Webelievethatthreequestionsmustbeansweredtogainadeeperunderstanding:(a)understandingwhy
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 27
MetricCategory SpecificMeasurements Rationale
Parameternorms Parameternormsperlayer Easytomeasure;first-stopdiagnostic
toolforoptimizationissues
Gradientmetrics L1/L2normsperlayer,gradientspectrum Foundationsofgradient-basedlearning;
likelyprecedeotherpathologies
Curvature LargestHessianeigenvalue Fundamentalinsightsintooptimization
landscape
Table3. Proposedstandardizedmetricsforplasticitylossevaluation.
successfulregularizerswork,(b)identifyingthecausalrelationshipsbetweenobservedpathologies,and(c)developing
methodstoquantifynon-stationarity.
Despitestrongempiricalevidencethatcertainregularizersconsistentlymitigateplasticityloss,theunderlying
mechanismsoftheseregularizersremainunclear.LayerNormisperhapsthemostsuccessfulintervention,yetwecannot
definitivelystatewhetheritsbenefitsarisefrommaintainingnormalizedactivations,providinggradientsthrough
normalizationstatistics,inducingimplicitlearningrateschedules,orrevivingdeadneurons[77–79,118].Similarly,
L2regularizationandL2Init[25]bothimproveplasticity,butitremainsunclearwhethertheyprimarilyworkby
controllingparameternormmagnitudesorthroughimplicitfunctionalregularization.SpectralNorm’sbenefitscould
stemfromenforcingLipschitzconstraints,fromimplicitlearningrateeffects,orfrombothmechanismsoperating
simultaneously[15,42,88].Thefieldneedsmechanisticstudiesthatisolateandtestindividualhypothesesratherthan
focusingonbenchmarkperformance.
Figure1depictsaplausiblecausalchain:non-stationaritypluslarge-meanregressionleadstogradientinstability,
whichcausesparameternormgrowth,whichproducespathologiesincludingsharplandscapes,saturatedunits,and
rankcollapse,ultimatelyreducingperformance.However,criticallinksremainpoorlyunderstood.Theconnection
betweenparameternormsandsharpnessexemplifiesthisgap.Lyleetal.[78]findanempiricalcorrelationbetween
parameternormsandmaximumHessianeigenvalues,butdonotestablishacausalrelationship.Whetherthiscorrelation
arisesfundamentallyduringthetrainingofneuralnetworkswithnon-stationarityorwhetheritisanartifactofspecific
architecturesandactivationfunctionsremainsunknown.Rankcollapseanddormantneuronscorrelatestrongly[45]in
offlineRL,butthecausaldirectionremainsunclearaswell.Bothmaybedownstreamconsequencesofgradientcollapse
fromparameternormgrowthratherthancausingeachother.
Whilenon-stationarityclearlycontributestoplasticityloss,theprecisemechanismsunderlyingthisphenomenon
remainelusive.IndeepRL,twoprimaryformsofnon-stationarityoccur:targetnon-stationarityfrombootstrapping
(Section2.2)andinputnon-stationarityfrompolicychanges[68].Evidencefromdifferentstudiesconflicts,withsome
emphasizingtargetshiftsandothershighlightingchangesininputdistribution[56,68,107].Morefundamentally,
thefieldlacksmethodstoquantifythedegreeofnon-stationarityinagivenlearningproblem.Suchquantification
isnecessaryforprincipledregularizationselection:strongernon-stationarityshouldrequirestrongerregularization,
butwithoutmeasurementtools,thisprinciplecannotbeimplemented.Additionally,plasticitylossoccursinboth
classificationandregressionundernon-stationarity[56,69,78],yetthesetaskshavedifferentlosslandscapesand
optimizationdynamics.Identifyingthecommonfactorslinkingnon-stationaritytoplasticitylossacrosssettingsremains
anopenquestion.
Preprint

28 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
6.3 ConnectionstoEstablishedRLIssues
ResearchonplasticitylosshasrevealedthatmanyclassicalRLproblemsrespondtogeneralneuralnetworkregulariza-
tionratherthandomain-specificalgorithmicsolutions.Overestimationbiashasmotivatedextensiveworkondouble
Q-learningandpessimisticvalueestimation[37,112],yetrecentbenchmarkssuggestplasticityinterventionsaddressit
moreeffectively[23,55,88].Explorationmaybedrivenpartiallybyfrequentactionchangesfromgradient-basedlearn-
inginsteadofexplicitmechanismslike𝜖-greedy[100,117].Moststrikingly,Baird’scounterexampledemonstratedthat
certaincombinationsofbootstrappingandfunctionapproximationmustdiverge;yet,LayerNormandL2regularization
stabilizethisexactcase[40].Recentadvancesinnormalizationhaveeliminatedtheneedforperceivedcornerstonesta-
bilitytechniques,suchastargetnetworks,alongsideBatchNormorLayerNorm.Despitethissimplification,performance
ismaintainedorimproved[13,40].
ThesefindingsdonotprovethatalldeepRLproblemsreducetooptimizationissues,buttheywarrantasystematic
revisitingofclassicalproblems.Considerthedeadlytriad:bootstrapping,functionapproximation,andoff-policylearning
cannotbesafelycombined[113].Isthisinstabilitytrulyinherent,ordoesitstemfrominsufficientregularization?
Similarly,passivelearningexhibitsdegradedperformancewhenlearningfromdatageneratedbyotherpolicies[98].Does
thisreflectafundamentaloff-policydifficultyornetworkoptimizationissuesduetodistributionshift?Testingwhether
plasticitymethodsresolvetheseclassicalfailureswouldclarifywhichproblemsarealgorithmicversusoptimization-
based,withdirectimplicationsforwhendomain-specificapproachesarerequiredversuswherestandarddeeplearning
regularizerssuffice.
6.4 TheoryDevelopment
Despitesubstantialempiricalprogress,welacktheoreticalframeworkstopredictwhenplasticitylosswilloccuror
whichinterventionswillworkforagivenproblem.Ratherthanaspiringtogeneralframeworks,weidentifyspecific
theoreticaladvancesthatwoulddirectlyinformpractice.
Canweboundtherateatwhichplasticityislostundernon-stationarityasafunctionofmeasurablepropertiessuch
astargetshiftmagnitude,batchsize,andlearningrate?Suchboundswouldpredicttheseverityofplasticitylossa
priori,ratherthandiscoveringitthroughextensiveexperimentation.Thisconnectstoamorefundamentalquestion
abouttherelationshipbetweenoptimizationdynamicsandplasticity:howdoesmaintainingplasticitythroughout
trainingaffecttotalsamplecomplexitytoreachtargetperformance?Formalizingthisrelationshipwouldquantifythe
practicalcostofplasticitylossandjustifythecomputationaloverheadofplasticity-preservingalgorithms.Acritical
missingpieceistheformalconnectionbetweenparameternormgrowthandlosslandscapecurvatureestablished
empiricallybyLyleetal.[78].HowexactlyareparameternormgrowthandthemaximumeigenvalueoftheHessian
connected? As previously mentioned, current understanding relies on empirical correlation rather than rigorous
derivation.Establishingthisconnectiontheoreticallywouldexplainacentralmechanismlinkingnon-stationarityto
optimizationdifficulty.Additionally,formalizingtheparameternorm-curvaturerelationshipmayrevealwhetherit
holdsuniversallyacrossarchitecturesordependsonspecificdesignchoices,suchasactivationfunctions,architecture,
orloss.
Categoricallossestypicallyoutperformregressionforplasticitypreservation[34,57,79].However,thisadvantage
isnotuniversal;inenvironmentslikeAtari’sPhoenixandAlien,MSEsubstantiallyoutperformsclassificationrefor-
mulations.Welackatheoreticaljustificationforwhyandwhencategoricallossesexcel.Regressiongradientsscale
withpredictionerror,potentiallycausingparameternormexplosionunderlarge-meantargets,whicharecommonin
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 29
value-basedRL.Cross-entropygradients,incontrast,remainboundedevenforlargetargetvalues.Doesthisbounded
gradientpropertyaloneexplainthebenefitsofcategoricallosses?Ordootherfactorscontributesubstantially,such
astheimplicitlabelsmoothingfromdistributingprobabilitymassbymethodslikeHL-Gauss[57]?Formalizingthese
mechanismswouldclarifywhencategoricalreformulationshelpandguidetheirdesignforothercontinuousprediction
problemsbeyondvaluefunctions.
7 Conclusion
PlasticitylossrepresentsafundamentalchallengeindeepRL,wherenetworksprogressivelylosetheirabilitytolearnde-
spiteremainingcapacity.Thissurveyconsolidatedfragmenteddefinitionsintoaunifiedformulation(Definition2.1)and
developedthefirstsystematictaxonomyoffactorsandmitigationstrategiesencompassingapproximatelyfiftymethods
acrosstwelvecategories(Figures4and2).Ouranalysisrevealsacentralfinding:generalregularizationtechniquestend
tooutperformdomain-specificplasticityinterventionsacrossdiversebenchmarks.Themostsuccessfulagentsoften
combinethesewell-establishedtechniquesratherthanrelyingonnovelRL-specificmechanisms.Thispatternextends
beyondplasticitylossitself,asgeneralregularizersalsomitigateoverestimationbias,improveexploration,andstabilize
trainingwherespecializedalgorithmswerepreviouslythoughtnecessary(Sections6.3).
Given these findings, we recommend that practitioners encountering plasticity loss should start with general
regularizationtechniquessuchasLayerNormandSpectralNorm.Thesemethodsoffertwoadvantages:theyfrequently
matchorexceedtheperformanceofspecializedapproaches,andtheybenefitfrombattle-tested,efficientimplementations
instandarddeeplearningframeworks.Whenadditionalinterventionisneeded,softresetsprovideaneffectivenext
stepduetotheirsimplicityandbroadapplicabilityacrosswarm-starting,on-policy,andoff-policysettings.
However,fundamentalunderstandingremainslimiteddespiteempiricalprogress.Plasticitylossmanifeststhrough
multiplemeasurablepathologies:dormantneurons,rankcollapse,parameternormgrowth,andgradientissues.Non-
stationarityclearlycontributesaswell,butneitheritsdegreenorwhichenvironmentstriggersevereplasticitylosscan
bepredicted.Compoundingthesegaps,thefieldlacksstandardizedevaluationprotocols,withresearchersdesigning
bespokeexperimentstrackingdifferentmetrics.CurrentworkalsofocusesonAtariandtheDeepMindControlSuite,
wheretheeffectivenessofmethodsvariesacrosstasks(Sections4and6.1).
Thehighestpriorityforfutureresearchisestablishingcausalmechanisms.InFigure1,wesynthesizetheexisting
driversandpathologiesofplasticitylossintoahypotheticalcausalmodel.Becausetheseassociationsareempirical
ratherthantheoreticallygrounded,thecausalrelationshipsremainunclear.Forexample,thecorrelationbetween
parameternormgrowthandlosslandscapecurvatureisknown,buttheirdirectionaldependenceisstillunknown.
Understandingwhysuccessfulregularizerswork,suchaswhichofLayerNorm’smultipleeffectsdriveitsbenefits,
remainsunresolved.GeneralregularizationmethodscanmitigateclassicalRLproblems,suchasoverestimationbias
andthedeadlytriad.Consequently,theseissuesmaystemfromoptimizationpathologieswhenusingRLwithdeep
learningratherthanfundamentalalgorithmiclimitations.Systematicallyrevisitingtheseclassicalproblemscouldclarify
whichchallengesgenuinelyrequiredomain-specificsolutions(Sections6.2,6.4).Webelievethatsuccessforthefield
willbemeasurednotbynovelalgorithmsbutbypredictivetheories:frameworksthatexplainwhenplasticityloss
willoccurbasedonmeasurableenvironmentandtrainingproperties,whyspecificregularizerssucceed,andhowto
selectinterventionsbasedonproblemcharacteristicsratherthanexhaustivesearch.Wehopethissurveyprovidesa
foundationformovingtowardsuchprincipled,mechanisticunderstanding.
Preprint

30 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
Acknowledgments
ThisworkhasbeenfundedinpartsbytheViennaScienceandTechnologyFund(WWTF)[10.47379/ICT20058].We
thankMateuszOstaszewskifortheinsightfuldiscussionsthatsubstantiallyimprovedourwork.
References
[1] ZaheerAbbas,RosieZhao,JosephModayil,AdamWhite,andMarlosC.Machado.2023. LossofPlasticityinContinualDeepReinforcement
Learning.InConferenceonLifelongLearningAgents(CoLLAs).620–636. https://proceedings.mlr.press/v232/abbas23a.html
[2] DavidAbel,AndréBarreto,BenjaminVanRoy,DoinaPrecup,HadoPhilipvanHasselt,andSatinderSingh.2023. ADefinitionofContinual
ReinforcementLearning.InAdvancesinNeuralInformationProcessingSystems(NeurIPS),AliceOh,TristanNaumann,AmirGloberson,Kate
Saenko,MoritzHardt,andSergeyLevine(Eds.). http://papers.nips.cc/paper_files/paper/2023/hash/9d8cf1247786d6dfeefeeb53b8b5f6d7-Abstract-
Conference.html
[3] MarcinAndrychowicz,AntonRaichuk,PiotrStanczyk,ManuOrsini,SertanGirgin,RaphaëlMarinier,LéonardHussenot,MatthieuGeist,
OlivierPietquin,MarcinMichalski,SylvainGelly,andOlivierBachem.2021. WhatMattersforOn-PolicyDeepActor-CriticMethods?A
Large-ScaleStudy.In9thInternationalConferenceonLearningRepresentations,ICLR2021,VirtualEvent,Austria,May3-7,2021.OpenReview.net.
https://openreview.net/forum?id=nIAxjsniDzg
[4] KavoshAsadi,RasoolFakoor,andShohamSabach.2023.ResettingtheOptimizerinDeepRL:AnEmpiricalStudy.InAdvancesinNeuralInformation
ProcessingSystems(NeurIPS). http://papers.nips.cc/paper_files/paper/2023/hash/e4bf5c3245fd92a4554a16af9803b757-Abstract-Conference.html
[5] JordanT.AshandRyanP.Adams.2020. OnWarm-StartingNeuralNetworkTraining.InAdvancesinNeuralInformationProcessingSystems
(NeurIPS). https://proceedings.neurips.cc/paper/2020/hash/288cd2567953f06e460a33951f55daaf-Abstract.html
[6] AbhijeetAwasthiandSunitaSarawagi.2019. ContinualLearningwithNeuralNetworks:AReview.InProceedingsoftheACMIndiaJoint
InternationalConferenceonDataScienceandManagementofData,COMAD/CODS2019,Kolkata,India,January3-5,2019,RaghuKrishnapuramand
ParagSingla(Eds.).ACM,362–365.doi:10.1145/3297001.3297062
[7] LeiJimmyBa,JamieRyanKiros,andGeoffreyE.Hinton.2016. LayerNormalization. CoRRabs/1607.06450(2016). arXiv:1607.06450 http:
//arxiv.org/abs/1607.06450
[8] MarcG.Bellemare,WillDabney,andRémiMunos.2017.ADistributionalPerspectiveonReinforcementLearning.InInternationalConferenceon
MachineLearning(ICML),Vol.70.449–458. http://proceedings.mlr.press/v70/bellemare17a.html
[9] MarcG.Bellemare,WillDabney,andMarkRowland.2023.DistributionalReinforcementLearning.MITPress. http://www.distributional-rl.org.
[10] MarcG.Bellemare,YavarNaddaf,JoelVeness,andMichaelBowling.2013.TheArcadeLearningEnvironment:AnEvaluationPlatformforGeneral
Agents.J.Artif.Intell.Res.47(2013),253–279.doi:10.1613/JAIR.3912
[11] TudorBerariu,WojciechCzarnecki,SohamDe,JörgBornschein,SamuelL.Smith,RazvanPascanu,andClaudiaClopath.2021.Astudyonthe
plasticityofneuralnetworks.CoRRabs/2106.00042(2021).arXiv:2106.00042 https://arxiv.org/abs/2106.00042
[12] ChristopherBerner,GregBrockman,BrookeChan,VickiCheung,PrzemyslawDebiak,ChristyDennison,DavidFarhi,QuirinFischer,Shariq
Hashme,ChristopherHesse,RafalJózefowicz,ScottGray,CatherineOlsson,JakubPachocki,MichaelPetrov,HenriquePondédeOliveiraPinto,
JonathanRaiman,TimSalimans,JeremySchlatter,JonasSchneider,SzymonSidor,IlyaSutskever,JieTang,FilipWolski,andSusanZhang.2019.
Dota2withLargeScaleDeepReinforcementLearning.CoRRabs/1912.06680(2019).arXiv:1912.06680 http://arxiv.org/abs/1912.06680
[13] AdityaBhatt,DanielPalenicek,BorisBelousov,MaxArgus,ArtemijAmiranashvili,ThomasBrox,andJanPeters.2024.CrossQ:BatchNormalization
inDeepReinforcementLearningforGreaterSampleEfficiencyandSimplicity.InInternationalConferenceonLearningRepresentations(ICLR).
[14] CelesteBiever.2023.ChatGPTbroketheTuringtest-theraceisonfornewwaystoassessAI.Nature619,7971(2023),686–689.
[15] JohanBjorck,CarlaP.Gomes,andKilianQ.Weinberger.2021. TowardsDeeperDeepReinforcementLearningwithSpectralNormalization.
8242–8255pages. https://proceedings.neurips.cc/paper/2021/hash/4588e674d3f0faf985047d4c3f13ed0d-Abstract.html
[16] JohanBjorck,CarlaP.Gomes,andKilianQ.Weinberger.2022.IsHighVarianceUnavoidableinRL?ACaseStudyinContinuousControl.In
InternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=9xhgmsNVHu
[17] EdoardoCetinandOyaÇeliktutan.2023.LearningPessimismforReinforcementLearning.InConferenceonArtificialIntelligence(AAAI),Brian
Williams,YilingChen,andJenniferNeville(Eds.).AAAIPress,6971–6979.doi:10.1609/AAAI.V37I6.25852
[18] XinyueChen,CheWang,ZijianZhou,andKeithW.Ross.2021.RandomizedEnsembledDoubleQ-Learning:LearningFastWithoutaModel.In
InternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=AY8zfZm0tDd
[19] WesleyChung,LynnCherif,DoinaPrecup,andDavidMeger.2024.ParsevalRegularizationforContinualReinforcementLearning.InAdvancesin
NeuralInformationProcessingSystems38:AnnualConferenceonNeuralInformationProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,
December10-15,2024,AmirGlobersons,LesterMackey,DanielleBelgrave,AngelaFan,UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.).
http://papers.nips.cc/paper_files/paper/2024/hash/e6df4efa20adf8ef9acb80e94072a429-Abstract-Conference.html
[20] MoustaphaCisse,PiotrBojanowski,EdouardGrave,YannDauphin,andNicolasUsunier.2017. Parsevalnetworks:Improvingrobustnessto
adversarialexamples.InInternationalconferenceonmachinelearning.PMLR,854–863.
[21] Djork-ArnéClevert,ThomasUnterthiner,andSeppHochreiter.2016.FastandAccurateDeepNetworkLearningbyExponentialLinearUnits
(ELUs).InInternationalConferenceonLearningRepresentations(ICLR),YoshuaBengioandYannLeCun(Eds.). http://arxiv.org/abs/1511.07289
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 31
[22] KarlCobbe,ChristopherHesse,JacobHilton,andJohnSchulman.2020.LeveragingProceduralGenerationtoBenchmarkReinforcementLearning.
InProceedingsofthe37thInternationalConferenceonMachineLearning,ICML2020,13-18July2020,VirtualEvent(ProceedingsofMachineLearning
Research,Vol.119).PMLR,2048–2056. http://proceedings.mlr.press/v119/cobbe20a.html
[23] QuentinDelfosse,PatrickSchramowski,MartinMundt,AlejandroMolina,andKristianKersting.2024.AdaptiveRationalActivationstoBoost
DeepReinforcementLearning.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=
g90ysX1sVs
[24] ShibhanshDohare,J.FernandoHernandez-Garcia,QingfengLan,ParashRahman,A.RupamMahmood,andRichardS.Sutton.2024.Lossof
plasticityindeepcontinuallearning.Nat.632,8026(2024),768–774.doi:10.1038/S41586-024-07711-7
[25] ShibhanshDohare,J.FernandoHernandez-Garcia,ParashRahman,RichardS.Sutton,andA.RupamMahmood.2023.MaintainingPlasticityin
DeepContinualLearning.CoRRabs/2306.13812(2023).arXiv:2306.13812doi:10.48550/ARXIV.2306.13812
[26] PierlucaD’Oro,MaxSchwarzer,EvgeniiNikishin,Pierre-LucBacon,MarcG.Bellemare,andAaronC.Courville.2023. Sample-EfficientRe-
inforcementLearningbyBreakingtheReplayRatioBarrier.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net.
https://openreview.net/pdf?id=OpC-9aBBVJe
[27] AndyEhrenberg,RobertKirk,MinqiJiang,EdwardGrefenstette,andTimRocktäschel.2022.Astudyofoff-policylearninginenvironmentswith
proceduralcontentgeneration.InICLRWorkshoponAgentLearninginOpen-Endedness.
[28] BenjaminEllis,MatthewThomasJackson,AndreiLupu,AlexanderDavidGoldie,MattieFellows,ShimonWhiteson,andJakobN.Foerster.2024.
AdamonLocalTime:AddressingNonstationarityinRLwithRelativeAdamTimesteps.InAdvancesinNeuralInformationProcessingSystems38:
AnnualConferenceonNeuralInformationProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,
LesterMackey,DanielleBelgrave,AngelaFan,UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.). http://papers.nips.cc/paper_files/paper/
2024/hash/f2733d3b0dde1d74995f35a9cf442d38-Abstract-Conference.html
[29] MohamedElsayed,QingfengLan,ClareLyle,andA.RupamMahmood.2024.WeightClippingforDeepContinualandReinforcementLearning.
RLJ5(2024),2198–2217.
[30] MohamedElsayedandA.RupamMahmood.2024.AddressingLossofPlasticityandCatastrophicForgettinginContinualLearning.InInternational
ConferenceonLearningRepresentations(ICLR). https://openreview.net/forum?id=sKPzAXoylB
[31] MohamedElsayed,GauthamVasan,andA.RupamMahmood.2024.StreamingDeepReinforcementLearningFinallyWorks.CoRRabs/2410.14606
(2024).arXiv:2410.14606doi:10.48550/ARXIV.2410.14606
[32] LoganEngstrom,AndrewIlyas,ShibaniSanturkar,DimitrisTsipras,FirdausJanoos,LarryRudolph,andAleksanderMadry.2020.Implementation
MattersinDeepPolicyGradients:ACaseStudyonPPOandTRPO.CoRRabs/2005.12729(2020).arXiv:2005.12729 https://arxiv.org/abs/2005.12729
[33] LasseEspeholt,HubertSoyer,RémiMunos,KarenSimonyan,VolodymyrMnih,TomWard,YotamDoron,VladFiroiu,TimHarley,IainDunning,
ShaneLegg,andKorayKavukcuoglu.2018.IMPALA:ScalableDistributedDeep-RLwithImportanceWeightedActor-LearnerArchitectures.In
InternationalConferenceonMachineLearning(ICML).1406–1415. http://proceedings.mlr.press/v80/espeholt18a.html
[34] JesseFarebrother,JordiOrbay,QuanVuong,AdrienAliTaïga,YevgenChebotar,TedXiao,AlexIrpan,SergeyLevine,PabloSamuelCastro,
AleksandraFaust,AviralKumar,andRishabhAgarwal.2024.StopRegressing:TrainingValueFunctionsviaClassificationforScalableDeepRL.In
InternationalConferenceonMachineLearning(ICML). https://openreview.net/forum?id=dVpFKfqF3R
[35] AlhusseinFawzi,MatejBalog,AjaHuang,ThomasHubert,BernardinoRomera-Paredes,MohammadaminBarekatain,AlexanderNovikov,
FranciscoJ.R.Ruiz,JulianSchrittwieser,GrzegorzSwirszcz,DavidSilver,DemisHassabis,andPushmeetKohli.2022.Discoveringfastermatrix
multiplicationalgorithmswithreinforcementlearning.Nat.610,7930(2022),47–53.doi:10.1038/S41586-022-05172-4
[36] PierreForet,ArielKleiner,HosseinMobahi,andBehnamNeyshabur.2021.Sharpness-awareMinimizationforEfficientlyImprovingGeneralization.
InInternationalConferenceonLearningRepresentations(ICLR). https://openreview.net/forum?id=6Tm1mposlrM
[37] ScottFujimoto,HerkevanHoof,andDavidMeger.2018.AddressingFunctionApproximationErrorinActor-CriticMethods.InInternational
ConferenceonMachineLearning(ICML).1582–1591. http://proceedings.mlr.press/v80/fujimoto18a.html
[38] AlexandreGalashov,MichalisK.Titsias,AndrásGyörgy,ClareLyle,RazvanPascanu,YeeWhyeTeh,andManeeshSahani.2024.Non-Stationary
LearningofNeuralNetworkswithAutomaticSoftParameterReset.InAdvancesinNeuralInformationProcessingSystems38:AnnualConference
onNeuralInformationProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,LesterMackey,
DanielleBelgrave,AngelaFan,UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.). http://papers.nips.cc/paper_files/paper/2024/hash/
978cc34c539fd26f0e8afb7e3905f34a-Abstract-Conference.html
[39] MatteoGallici,MattieFellows,BenjaminEllis,BartomeuPou,IvanMasmitja,JakobNicolausFoerster,andMarioMartin.2025.SimplifyingDeep
TemporalDifferenceLearning.InTheThirteenthInternationalConferenceonLearningRepresentations,ICLR2025,Singapore,April24-28,2025.
OpenReview.net. https://openreview.net/forum?id=7IzeL0kflu
[40] MatteoGallici,MattieFellows,BenjaminEllis,BartomeuPou,IvanMasmitja,JakobNicolausFoerster,andMarioMartin.2025.SimplifyingDeep
TemporalDifferenceLearning.InTheThirteenthInternationalConferenceonLearningRepresentations,ICLR2025,Singapore,April24-28,2025.
OpenReview.net. https://openreview.net/forum?id=7IzeL0kflu
[41] LukeB.Godfrey.2019.AnEvaluationofParametricActivationFunctionsforDeepLearning.InInternationalConferenceonSystems,Manand
Cybernetics(SMC).IEEE,3006–3011.doi:10.1109/SMC.2019.8913972
[42] FlorinGogianu,TudorBerariu,MihaelaRosca,ClaudiaClopath,LucianBusoniu,andRazvanPascanu.2021.SpectralNormalisationforDeep
ReinforcementLearning:AnOptimisationPerspective.InInternationalConferenceonMachineLearning(ICML).3734–3744. http://proceedings.
Preprint

32 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
mlr.press/v139/gogianu21a.html
[43] AlexanderDavidGoldie,ChrisLu,MatthewThomasJackson,ShimonWhiteson,andJakobN.Foerster.2024.CanLearnedOptimizationMake
ReinforcementLearningLessDifficult?.InAdvancesinNeuralInformationProcessingSystems38:AnnualConferenceonNeuralInformationProcessing
Systems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,LesterMackey,DanielleBelgrave,AngelaFan,Ulrich
Paquet,JakubM.Tomczak,andChengZhang(Eds.). http://papers.nips.cc/paper_files/paper/2024/hash/09e1944b7f2372f9f81866470c59b663-
Abstract-Conference.html
[44] IanJGoodfellow,MehdiMirza,DaXiao,AaronCourville,andYoshuaBengio.2013. Anempiricalinvestigationofcatastrophicforgettingin
gradient-basedneuralnetworks.arXivpreprintarXiv:1312.6211(2013).
[45] ÇaglarGülçehre,SrivatsanSrinivasan,JakubSygnowski,GeorgOstrovski,MehrdadFarajtabar,MatthewHoffman,RazvanPascanu,andArnaud
Doucet.2022.AnempiricalstudyofimplicitregularizationindeepofflineRL.MachineLearningResearch2022(2022). https://openreview.net/
forum?id=HFfJWx60IT
[46] TuomasHaarnoja,AurickZhou,PieterAbbeel,andSergeyLevine.2018.SoftActor-Critic:Off-PolicyMaximumEntropyDeepReinforcement
LearningwithaStochasticActor.InInternationalConferenceonMachineLearning(ICML).1856–1865. http://proceedings.mlr.press/v80/haarnoja18b.
html
[47] KaimingHe,XiangyuZhang,ShaoqingRen,andJianSun.2016.DeepResidualLearningforImageRecognition.InConferenceonComputerVision
andPatternRecognition(CVPR).IEEE,770–778.doi:10.1109/CVPR.2016.90
[48] QiangHe,TianyiZhou,MengFang,andSetarehMaghsudi.2024.AdaptiveRegularizationofRepresentationRankasanImplicitConstraintof
BellmanEquation.InInternationalConferenceonLearningRepresentations(ICLR). https://openreview.net/forum?id=apXtolxDaJ
[49] GeoffreyE.Hinton,OriolVinyals,andJeffreyDean.2015. DistillingtheKnowledgeinaNeuralNetwork. CoRRabs/1503.02531(2015).
arXiv:1503.02531 http://arxiv.org/abs/1503.02531
[50] SeppHochreiter.1998.TheVanishingGradientProblemDuringLearningRecurrentNeuralNetsandProblemSolutions.Int.J.Uncertain.Fuzziness
Knowl.BasedSyst.6,2(1998),107–116.
[51] SeppHochreiterandJürgenSchmidhuber.1997.FlatMinima.NeuralComputation9,1(011997),1–42. arXiv:https://direct.mit.edu/neco/article-
pdf/9/1/1/813385/neco.1997.9.1.1.pdfdoi:10.1162/neco.1997.9.1.1
[52] ShengyiHuang,RousslanFernandJulienDossa,AntoninRaffin,AnssiKanervisto,andWeixunWang.2022.The37ImplementationDetailsof
ProximalPolicyOptimization.InICLRBlogTrack. https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/https://iclr-blog-
track.github.io/2022/03/25/ppo-implementation-details/.
[53] ShengyiHuang,RousslanFernandJulienDossa,ChangYe,JeffBraga,DipamChakraborty,KinalMehta,andJoãoG.M.Araújo.2022.CleanRL:
High-qualitySingle-fileImplementationsofDeepReinforcementLearningAlgorithms. J.Mach.Learn.Res.23(2022),274:1–274:18. https:
//jmlr.org/papers/v23/21-1342.html
[54] MinyoungHuh,HosseinMobahi,RichardZhang,BrianCheung,PulkitAgrawal,andPhillipIsola.2023.TheLow-RankSimplicityBiasinDeep
Networks.Trans.Mach.Learn.Res.2023(2023). https://openreview.net/forum?id=bCiNWDmlY2
[55] MarcelHussing,ClaasVoelcker,IgorGilitschenski,Amir-massoudFarahmand,andEricEaton.2024.DissectingDeepRLwithHighUpdateRatios:
CombattingValueDivergence.RLJ2(2024),995–1018.
[56] MaximilianIgl,GregoryFarquhar,JelenaLuketina,WendelinBoehmer,andShimonWhiteson.2021.TransientNon-stationarityandGeneralisation
inDeepReinforcementLearning.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?
id=Qun8fv4qSby
[57] EhsanImaniandMarthaWhite.2018.ImprovingRegressionPerformancewithDistributionalLosses.InInternationalConferenceonMachine
Learning(ICML)(ProceedingsofMachineLearningResearch,Vol.80),JenniferG.DyandAndreasKrause(Eds.).PMLR,2162–2171. http:
//proceedings.mlr.press/v80/imani18a.html
[58] SergeyIoffeandChristianSzegedy.2015.BatchNormalization:AcceleratingDeepNetworkTrainingbyReducingInternalCovariateShift.In
InternationalConferenceonMachineLearning(ICML)(JMLRWorkshopandConferenceProceedings,Vol.37),FrancisR.BachandDavidM.Blei
(Eds.).JMLR.org,448–456. http://proceedings.mlr.press/v37/ioffe15.html
[59] TianyingJi,YongyuanLiang,YanZeng,YuLuo,GuoweiXu,JiaweiGuo,RuijieZheng,FurongHuang,FuchunSun,andHuazheXu.2024.ACE:
Off-PolicyActor-CriticwithCausality-AwareEntropyRegularization.InInternationalConferenceonMachineLearning(ICML).OpenReview.net.
https://openreview.net/forum?id=1puvYh729M
[60] ArthurJulianiandJordanT.Ash.2024.AStudyofPlasticityLossinOn-PolicyDeepReinforcementLearning.InAdvancesinNeuralInformation
ProcessingSystems38:AnnualConferenceonNeuralInformationProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,December10-
15,2024,AmirGlobersons,LesterMackey,DanielleBelgrave,AngelaFan,UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.). http:
//papers.nips.cc/paper_files/paper/2024/hash/ce7984e36d58659211a8dc7d5457cd6f-Abstract-Conference.html
[61] LukaszKaiser,MohammadBabaeizadeh,PiotrMilos,BlazejOsinski,RoyH.Campbell,KonradCzechowski,DumitruErhan,ChelseaFinn,Piotr
Kozakowski,SergeyLevine,AfrozMohiuddin,RyanSepassi,GeorgeTucker,andHenrykMichalewski.2020.ModelBasedReinforcementLearning
forAtari.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=S1xCPJHtDB
[62] KhimyaKhetarpal,MatthewRiemer,IrinaRish,andDoinaPrecup.2022.TowardsContinualReinforcementLearning:AReviewandPerspectives.
J.Artif.Intell.Res.75(2022),1401–1476.doi:10.1613/JAIR.1.13673
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 33
[63] DiederikP.KingmaandJimmyBa.2015.Adam:AMethodforStochasticOptimization.InInternationalConferenceonLearningRepresentations
(ICLR),YoshuaBengioandYannLeCun(Eds.). http://arxiv.org/abs/1412.6980
[64] JacobEKooi,MarkHoogendoorn,andVincentFrançois-Lavet.2024.HadamardRepresentations:AugmentingHyperbolicTangentsinRL.arXiv
preprintarXiv:2406.09079(2024).
[65] AviralKumar,RishabhAgarwal,DibyaGhosh,andSergeyLevine.2021.ImplicitUnder-ParameterizationInhibitsData-EfficientDeepReinforcement
Learning.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=O9bnihsFfXU
[66] AviralKumar,RishabhAgarwal,TengyuMa,AaronC.Courville,GeorgeTucker,andSergeyLevine.2022.DR3:Value-BasedDeepReinforcement
LearningRequiresExplicitRegularization.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.
net/forum?id=POvMvLi91f
[67] MichaelLaskin,KiminLee,AdamStooke,LerrelPinto,PieterAbbeel,andAravindSrinivas.2020.ReinforcementLearningwithAugmentedData.
InAdvancesinNeuralInformationProcessingSystems(NeurIPS),HugoLarochelle,Marc’AurelioRanzato,RaiaHadsell,Maria-FlorinaBalcan,and
Hsuan-TienLin(Eds.). https://proceedings.neurips.cc/paper/2020/hash/e615c82aba461681ade82da2da38004a-Abstract.html
[68] HojoonLee,HanseulCho,HyunseungKim,DaehoonGwak,JoonkeeKim,JaegulChoo,Se-YoungYun,andChulheeYun.2023. PLASTIC:
ImprovingInputandLabelPlasticityforSampleEfficientReinforcementLearning.InAdvancesinNeuralInformationProcessingSystems(NeurIPS),
AliceOh,TristanNaumann,AmirGloberson,KateSaenko,MoritzHardt,andSergeyLevine(Eds.). http://papers.nips.cc/paper_files/paper/2023/
hash/c464fc4516aca4e68f2a14e67c6f0402-Abstract-Conference.html
[69] HojoonLee,HyeonseoCho,HyunseungKim,DonghuKim,DugkiMin,JaegulChoo,andClareLyle.2024. SlowandSteadyWinstheRace:
MaintainingPlasticitywithHareandTortoiseNetworks.InInternationalConferenceonMachineLearning(ICML).OpenReview.net. https:
//openreview.net/forum?id=VF177x7Syw
[70] HojoonLee,DongyoonHwang,DonghuKim,HyunseungKim,JunJetTai,KaushikSubramanian,PeterR.Wurman,JaegulChoo,PeterStone,and
TakumaSeno.2025.SimBa:SimplicityBiasforScalingUpParametersinDeepReinforcementLearning.InTheThirteenthInternationalConference
onLearningRepresentations,ICLR2025,Singapore,April24-28,2025.OpenReview.net. https://openreview.net/forum?id=jXLiDKsuDo
[71] AlexLewandowski,MichalBortkiewicz,SaurabhKumar,AndrásGyörgy,DaleSchuurmans,MateuszOstaszewski,andMarlosC.Machado.2025.
LearningContinuallybySpectralRegularization.InTheThirteenthInternationalConferenceonLearningRepresentations,ICLR2025,Singapore,April
24-28,2025.OpenReview.net. https://openreview.net/forum?id=Hcb2cgPbMg
[72] AlexLewandowski,DaleSchuurmans,andMarlosC.Machado.2025.PlasticLearningwithDeepFourierFeatures.InTheThirteenthInternational
ConferenceonLearningRepresentations,ICLR2025,Singapore,April24-28,2025.OpenReview.net. https://openreview.net/forum?id=NIkfix2eDQ
[73] AlexLewandowski,HarutoTanaka,DaleSchuurmans,andMarlosC.Machado.2023.CurvatureExplainsLossofPlasticity.CoRRabs/2312.00246
(2023).arXiv:2312.00246doi:10.48550/ARXIV.2312.00246
[74] JiashunLiu,JohanS.Obando-Ceron,AaronC.Courville,andLingPan.2025.NeuroplasticExpansioninDeepReinforcementLearning.InThe
ThirteenthInternationalConferenceonLearningRepresentations,ICLR2025,Singapore,April24-28,2025.OpenReview.net. https://openreview.net/
forum?id=20qZK2T7fa
[75] ClareLyle,MarkRowland,andWillDabney.2022.UnderstandingandPreventingCapacityLossinReinforcementLearning.InInternational
ConferenceonLearningRepresentations(ICLR). https://openreview.net/forum?id=ZkC8wKoLbQ7
[76] ClareLyle,MarkRowland,GeorgOstrovski,andWillDabney.2021.OntheEffectofAuxiliaryTasksonRepresentationDynamics.InInternational
ConferenceonArtificialIntelligenceandStatistics(AISTATS)(ProceedingsofMachineLearningResearch,Vol.130),ArindamBanerjeeandKenji
Fukumizu(Eds.).PMLR,1–9. http://proceedings.mlr.press/v130/lyle21a.html
[77] ClareLyle,ZeyuZheng,KhimyaKhetarpal,JamesMartens,HadoPhilipvanHasselt,RazvanPascanu,andWillDabney.2024.Normalizationand
effectivelearningratesinreinforcementlearning.InAdvancesinNeuralInformationProcessingSystems38:AnnualConferenceonNeuralInformation
ProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,LesterMackey,DanielleBelgrave,AngelaFan,
UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.).http://papers.nips.cc/paper_files/paper/2024/hash/c04d37be05ba74419d2d5705972a9d64-
Abstract-Conference.html
[78] ClareLyle,ZeyuZheng,KhimyaKhetarpal,HadovanHasselt,RazvanPascanu,JamesMartens,andWillDabney.2024.DisentanglingtheCauses
ofPlasticityLossinNeuralNetworks.InConferenceonLifelongLearningAgents,29-1August2024,UniversityofPisa,Pisa,Italy(Proceedingsof
MachineLearningResearch,Vol.274),VincenzoLomonaco,StefanoMelacci,TinneTuytelaars,SarathChandar,andRazvanPascanu(Eds.).PMLR,
750–783. https://proceedings.mlr.press/v274/lyle25a.html
[79] ClareLyle,ZeyuZheng,EvgeniiNikishin,BernardoÁvilaPires,RazvanPascanu,andWillDabney.2023.UnderstandingPlasticityinNeural
Networks.InInternationalConferenceonMachineLearning(ICML),Vol.202.23190–23211. https://proceedings.mlr.press/v202/lyle23b.html
[80] GuozhengMa,LuLi,SenZhang,ZixuanLiu,ZhenWang,YixinChen,LiShen,XueqianWang,andDachengTao.2024.RevisitingPlasticityin
VisualReinforcementLearning:Data,ModulesandTrainingStages.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net.
https://openreview.net/forum?id=0aR1s9YxoL
[81] AndrewLMaas,AwniYHannun,AndrewYNg,etal.2013.Rectifiernonlinearitiesimproveneuralnetworkacousticmodels.InInternational
ConferenceonMachineLearning(ICML)(JMLRWorkshopandConferenceProceedings,Vol.28).JMLR.org. http://robotics.stanford.edu/~amaas/
papers/relu_hybrid_icml2013_final.pdf
[82] AndrewKachitesMcCallum.1996.Reinforcementlearningwithselectiveperceptionandhiddenstate.UniversityofRochester.
Preprint

34 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
[83] EdanMeyer,AdamWhite,andMarlosC.Machado.2023.HarnessingDiscreteRepresentationsForContinualReinforcementLearning.CoRR
abs/2312.01203(2023).arXiv:2312.01203doi:10.48550/ARXIV.2312.01203
[84] TakeruMiyato,ToshikiKataoka,MasanoriKoyama,andYuichiYoshida.2018.SpectralNormalizationforGenerativeAdversarialNetworks.In
6thInternationalConferenceonLearningRepresentations,ICLR2018,Vancouver,BC,Canada,April30-May3,2018,ConferenceTrackProceedings.
OpenReview.net. https://openreview.net/forum?id=B1QRgziT-
[85] VolodymyrMnih,KorayKavukcuoglu,DavidSilver,AndreiA.Rusu,JoelVeness,MarcG.Bellemare,AlexGraves,MartinA.Riedmiller,Andreas
Fidjeland,GeorgOstrovski,StigPetersen,CharlesBeattie,AmirSadik,IoannisAntonoglou,HelenKing,DharshanKumaran,DaanWierstra,
ShaneLegg,andDemisHassabis.2015.Human-levelcontrolthroughdeepreinforcementlearning.Nat.518,7540(2015),529–533.doi:10.1038/
NATURE14236
[86] SkanderMoalla,AndreaMiele,DaniilPyatko,RazvanPascanu,andCaglarGulcehre.2024.NoRepresentation,NoTrust:ConnectingRepresentation,
Collapse,andTrustIssuesinPPO.InAdvancesinNeuralInformationProcessingSystems38:AnnualConferenceonNeuralInformationProcessing
Systems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,LesterMackey,DanielleBelgrave,AngelaFan,Ulrich
Paquet,JakubM.Tomczak,andChengZhang(Eds.). http://papers.nips.cc/paper_files/paper/2024/hash/81166fbd9cc5adf14031cdb69d3fd6a8-
Abstract-Conference.html
[87] KevinP.Murphy.2022.ProbabilisticMachineLearning:AnIntroduction.TheMITPress,Cambridge,Massachusetts.
[88] MichalNauman,MichalBortkiewicz,PiotrMilos,TomaszTrzcinski,MateuszOstaszewski,andMarekCygan.2024.Overestimation,Overfitting,and
PlasticityinActor-Critic:theBitterLessonofReinforcementLearning.InInternationalConferenceonMachineLearning(ICML).OpenReview.net.
https://openreview.net/forum?id=5vZzmCeTYu
[89] MichalNauman,MateuszOstaszewski,KrzysztofJankowski,PiotrMilos,andMarekCygan.2024.Bigger,Regularized,Optimistic:scalingfor
computeandsampleefficientcontinuouscontrol.InAdvancesinNeuralInformationProcessingSystems38:AnnualConferenceonNeuralInformation
ProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,LesterMackey,DanielleBelgrave,AngelaFan,
UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.). http://papers.nips.cc/paper_files/paper/2024/hash/cd3b5d2ed967e906af24b33d6a356cac-
Abstract-Conference.html
[90] EvgeniiNikishin,JunhyukOh,GeorgOstrovski,ClareLyle,RazvanPascanu,WillDabney,andAndréBarreto.2023.DeepReinforcementLearning
withPlasticityInjection.InAdvancesinNeuralInformationProcessingSystems(NeurIPS). http://papers.nips.cc/paper_files/paper/2023/hash/
75101364dc3aa7772d27528ea504472b-Abstract-Conference.html
[91] EvgeniiNikishin,MaxSchwarzer,PierlucaD’Oro,Pierre-LucBacon,andAaronC.Courville.2022.ThePrimacyBiasinDeepReinforcement
Learning.InInternationalConferenceonMachineLearning(ICML)(ProceedingsofMachineLearningResearch,Vol.162),KamalikaChaudhuri,Stefanie
Jegelka,LeSong,CsabaSzepesvári,GangNiu,andSivanSabato(Eds.).PMLR,16828–16847. https://proceedings.mlr.press/v162/nikishin22a.html
[92] JohanS.Obando-Ceron,JoãoGuilhermeMadeiraAraújo,AaronC.Courville,andPabloSamuelCastro.2024.Ontheconsistencyofhyper-parameter
selectioninvalue-baseddeepreinforcementlearning.RLJ3(2024),1037–1059. https://rlj.cs.umass.edu/2024/papers/Paper128.html
[93] JohanS.Obando-Ceron,MarcG.Bellemare,andPabloSamuelCastro.2023. Smallbatchdeepreinforcementlearning.InAdvancesinNeural
InformationProcessingSystems(NeurIPS),AliceOh,TristanNaumann,AmirGloberson,KateSaenko,MoritzHardt,andSergeyLevine(Eds.).
http://papers.nips.cc/paper_files/paper/2023/hash/528388f1ad3a481249a97cbb698d2fe6-Abstract-Conference.html
[94] JohanSamirObando-Ceron,AaronC.Courville,andPabloSamuelCastro.2024.Invalue-baseddeepreinforcementlearning,aprunednetworkis
agoodnetwork.InInternationalConferenceonMachineLearning(ICML).OpenReview.net. https://openreview.net/forum?id=seo9V9QRZp
[95] JohanSamirObando-Ceron,GhadaSokar,TimonWilli,ClareLyle,JesseFarebrother,JakobNicolausFoerster,GintareKarolinaDziugaite,Doina
Precup,andPabloSamuelCastro.2024.MixturesofExpertsUnlockParameterScalingforDeepRL.InForty-firstInternationalConferenceon
MachineLearning,ICML2024,Vienna,Austria,July21-27,2024.OpenReview.net. https://openreview.net/forum?id=X9VMhfFxwn
[96] OpenAI,IlgeAkkaya,MarcinAndrychowicz,MaciekChociej,MateuszLitwin,BobMcGrew,ArthurPetron,AlexPaino,MatthiasPlappert,Glenn
Powell,RaphaelRibas,JonasSchneider,NikolasTezak,JerryTworek,PeterWelinder,LilianWeng,QimingYuan,WojciechZaremba,andLei
Zhang.2019.SolvingRubik’sCubewithaRobotHand.CoRRabs/1910.07113(2019).arXiv:1910.07113 http://arxiv.org/abs/1910.07113
[97] GeorgOstrovski,MarcG.Bellemare,AäronvandenOord,andRémiMunos.2017.Count-BasedExplorationwithNeuralDensityModels.In
InternationalConferenceonMachineLearning(ICML)(ProceedingsofMachineLearningResearch,Vol.70),DoinaPrecupandYeeWhyeTeh(Eds.).
PMLR,2721–2730. http://proceedings.mlr.press/v70/ostrovski17a.html
[98] GeorgOstrovski,PabloSamuelCastro,andWillDabney.2021.TheDifficultyofPassiveLearninginDeepReinforcementLearning.InAdvancesin
NeuralInformationProcessingSystems34(NeurIPS),Marc’AurelioRanzato,AlinaBeygelzimer,YannN.Dauphin,PercyLiang,andJenniferWortman
Vaughan(Eds.).23283–23295. https://proceedings.neurips.cc/paper/2021/hash/c3e0c62ee91db8dc7382bde7419bb573-Abstract.html
[99] AdamPaszke,SamGross,FranciscoMassa,AdamLerer,JamesBradbury,GregoryChanan,TrevorKilleen,ZemingLin,NataliaGimelshein,Luca
Antiga,AlbanDesmaison,AndreasKöpf,EdwardZ.Yang,ZacharyDeVito,MartinRaison,AlykhanTejani,SasankChilamkurthy,BenoitSteiner,
LuFang,JunjieBai,andSoumithChintala.2019.PyTorch:AnImperativeStyle,High-PerformanceDeepLearningLibrary.InAdvancesinNeural
InformationProcessingSystems32(NeurIPS),HannaM.Wallach,HugoLarochelle,AlinaBeygelzimer,Florenced’Alché-Buc,EmilyB.Fox,and
RomanGarnett(Eds.).8024–8035. https://proceedings.neurips.cc/paper/2019/hash/bdbca288fee7f92f2bfa9f7012727740-Abstract.html
[100] TomSchaul,AndréBarreto,JohnQuan,andGeorgOstrovski.2022.ThePhenomenonofPolicyChurn.InAdvancesinNeuralInformationProcessing
Systems(NeurIPS),SanmiKoyejo,S.Mohamed,A.Agarwal,DanielleBelgrave,K.Cho,andA.Oh(Eds.). http://papers.nips.cc/paper_files/paper/
2022/hash/114292cf3f930ba157ed33f66997fee2-Abstract-Conference.html
Preprint

PlasticityLossinDeepReinforcementLearning:ASurvey 35
[101] JulianSchrittwieser,IoannisAntonoglou,ThomasHubert,KarenSimonyan,LaurentSifre,SimonSchmitt,ArthurGuez,EdwardLockhart,Demis
Hassabis,ThoreGraepel,TimothyP.Lillicrap,andDavidSilver.2020.MasteringAtari,Go,chessandshogibyplanningwithalearnedmodel.Nat.
588,7839(2020),604–609.doi:10.1038/S41586-020-03051-4
[102] JohnSchulman,FilipWolski,PrafullaDhariwal,AlecRadford,andOlegKlimov.2017. ProximalPolicyOptimizationAlgorithms. CoRR
abs/1707.06347(2017).arXiv:1707.06347 http://arxiv.org/abs/1707.06347
[103] MaxSchwarzer,JohanSamirObando-Ceron,AaronC.Courville,MarcG.Bellemare,RishabhAgarwal,andPabloSamuelCastro.2023.Bigger,
Better,Faster:Human-levelAtariwithhuman-levelefficiency.InInternationalConferenceonMachineLearning(ICML)(ProceedingsofMachine
LearningResearch,Vol.202),AndreasKrause,EmmaBrunskill,KyunghyunCho,BarbaraEngelhardt,SivanSabato,andJonathanScarlett(Eds.).
PMLR,30365–30380. https://proceedings.mlr.press/v202/schwarzer23a.html
[104] WenlingShang,KihyukSohn,DiogoAlmeida,andHonglakLee.2016. UnderstandingandImprovingConvolutionalNeuralNetworksvia
ConcatenatedRectifiedLinearUnits.InInternationalConferenceonMachineLearning(ICML)(JMLRWorkshopandConferenceProceedings,Vol.48),
Maria-FlorinaBalcanandKilianQ.Weinberger(Eds.).JMLR.org,2217–2225. http://proceedings.mlr.press/v48/shang16.html
[105] HaizhouShi,ZihaoXu,HengyiWang,WeiyiQin,WenyuanWang,YibinWang,andHaoWang.2024.ContinualLearningofLargeLanguage
Models:AComprehensiveSurvey.CoRRabs/2404.16789(2024).arXiv:2404.16789doi:10.48550/ARXIV.2404.16789
[106] DavidSilver,AjaHuang,ChrisJ.Maddison,ArthurGuez,LaurentSifre,GeorgevandenDriessche,JulianSchrittwieser,IoannisAntonoglou,
VedavyasPanneershelvam,MarcLanctot,SanderDieleman,DominikGrewe,JohnNham,NalKalchbrenner,IlyaSutskever,TimothyP.Lillicrap,
MadeleineLeach,KorayKavukcuoglu,ThoreGraepel,andDemisHassabis.2016.MasteringthegameofGowithdeepneuralnetworksandtree
search.Nat.529,7587(2016),484–489.doi:10.1038/NATURE16961
[107] GhadaSokar,RishabhAgarwal,PabloSamuelCastro,andUtkuEvci.2023.TheDormantNeuronPhenomenoninDeepReinforcementLearning.
InInternationalConferenceonMachineLearning(ICML)(ProceedingsofMachineLearningResearch,Vol.202),AndreasKrause,EmmaBrunskill,
KyunghyunCho,BarbaraEngelhardt,SivanSabato,andJonathanScarlett(Eds.).PMLR,32145–32168. https://proceedings.mlr.press/v202/sokar23a.
html
[108] RichardS.SuttonandAndrewG.Barto.1998.Reinforcementlearning-anintroduction.MITPress. https://www.worldcat.org/oclc/37293240
[109] YuvalTassa,YotamDoron,AlistairMuldal,TomErez,YazheLi,DiegodeLasCasas,DavidBudden,AbbasAbdolmaleki,JoshMerel,Andrew
Lefrancq,TimothyP.Lillicrap,andMartinA.Riedmiller.2018. DeepMindControlSuite. CoRRabs/1801.00690(2018). arXiv:1801.00690
http://arxiv.org/abs/1801.00690
[110] EmanuelTodorov,TomErez,andYuvalTassa.2012.MuJoCo:Aphysicsengineformodel-basedcontrol.In2012IEEE/RSJInternationalConference
onIntelligentRobotsandSystems,IROS2012,Vilamoura,Algarve,Portugal,October7-12,2012.IEEE,5026–5033.doi:10.1109/IROS.2012.6386109
[111] AäronvandenOord,OriolVinyals,andKorayKavukcuoglu.2017.NeuralDiscreteRepresentationLearning.InAdvancesinNeuralInformation
ProcessingSystems30:AnnualConferenceonNeuralInformationProcessingSystems2017,December4-9,2017,LongBeach,CA,USA,Isabelle
Guyon,UlrikevonLuxburg,SamyBengio,HannaM.Wallach,RobFergus,S.V.N.Vishwanathan,andRomanGarnett(Eds.).6306–6315.
https://proceedings.neurips.cc/paper/2017/hash/7a98af17e63a0ac09ce2e96d03992fbc-Abstract.html
[112] HadovanHasselt.2010.DoubleQ-learning.InAdvancesinNeuralInformationProcessingSystems(NeurIPS),JohnD.Lafferty,ChristopherK.I.
Williams,JohnShawe-Taylor,RichardS.Zemel,andAronCulotta(Eds.).CurranAssociates,Inc.,2613–2621. https://proceedings.neurips.cc/
paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html
[113] HadovanHasselt,YotamDoron,FlorianStrub,MatteoHessel,NicolasSonnerat,andJosephModayil.2018.DeepReinforcementLearningandthe
DeadlyTriad.CoRRabs/1812.02648(2018).arXiv:1812.02648 http://arxiv.org/abs/1812.02648
[114] GauthamVasan,MohamedElsayed,SeyedAlirezaAzimi,JiaminHe,FahimShahriar,ColinBellinger,MarthaWhite,andRupamMahmood.2024.
DeepPolicyGradientMethodsWithoutBatchUpdates,TargetNetworks,orReplayBuffers.InAdvancesinNeuralInformationProcessingSystems
38:AnnualConferenceonNeuralInformationProcessingSystems2024,NeurIPS2024,Vancouver,BC,Canada,December10-15,2024,AmirGlobersons,
LesterMackey,DanielleBelgrave,AngelaFan,UlrichPaquet,JakubM.Tomczak,andChengZhang(Eds.). http://papers.nips.cc/paper_files/paper/
2024/hash/019ef89617d539b15ed610ce8d1b76e1-Abstract-Conference.html
[115] ThéoVincent,FabianWahren,JanPeters,BorisBelousov,andCarloD’Eramo.2025. AdaptiveQ-Network:On-the-flyTargetSelectionfor
DeepReinforcementLearning.InTheThirteenthInternationalConferenceonLearningRepresentations,ICLR2025,Singapore,April24-28,2025.
OpenReview.net. https://openreview.net/forum?id=leACdxBEgv
[116] LiyuanWang,XingxingZhang,HangSu,andJunZhu.2024.AComprehensiveSurveyofContinualLearning:Theory,MethodandApplication.
IEEETrans.PatternAnal.Mach.Intell.46,8(2024),5362–5383.doi:10.1109/TPAMI.2024.3367329
[117] GuoweiXu,RuijieZheng,YongyuanLiang,XiyaoWang,ZhechengYuan,TianyingJi,YuLuo,XiaoyuLiu,JiaxinYuan,PuHua,ShuzhenLi,Yanjie
Ze,HalDauméIII,FurongHuang,andHuazheXu.2024.DrM:MasteringVisualReinforcementLearningthroughDormantRatioMinimization.In
InternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=MSe8YFbhUE
[118] JingjingXu,XuSun,ZhiyuanZhang,GuangxiangZhao,andJunyangLin.2019.UnderstandingandImprovingLayerNormalization.InAdvances
inNeuralInformationProcessingSystems32(NeurIPS),HannaM.Wallach,HugoLarochelle,AlinaBeygelzimer,Florenced’Alché-Buc,EmilyB.Fox,
andRomanGarnett(Eds.).4383–4393. https://proceedings.neurips.cc/paper/2019/hash/2f4fe03d77724a7217006e5d16728874-Abstract.html
[119] DenisYarats,RobFergus,AlessandroLazaric,andLerrelPinto.2022.MasteringVisualContinuousControl:ImprovedData-AugmentedReinforce-
mentLearning.InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=_SJ-_yyes8
Preprint

36 Klein,Luther,McAuliffe,Miklautz,Plant,andTschiatschek
[120] DenisYarats,IlyaKostrikov,andRobFergus.2021.ImageAugmentationIsAllYouNeed:RegularizingDeepReinforcementLearningfromPixels.
InInternationalConferenceonLearningRepresentations(ICLR).OpenReview.net. https://openreview.net/forum?id=GY6-6sTvGaf
Preprint