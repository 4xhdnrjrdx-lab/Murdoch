from pathlib import Path
from docx import Document
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1]
p=R/'Original_User_Copy.docx'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='71d7175775b6e7ca45604c7920e5d8076c84e0ec7bff2c2f281dc86d1cae278c'
d=Document(p)
changes={
6:[
('Carrefour UAE brings tangible food and services that enable shoppers to identify, compare and pay for their foods.','Carrefour UAE combines groceries with services that help shoppers find, compare and pay for them.'),
('UAE business is managed','The UAE business is managed'),
('It has added 11 more UAE Carrefour outlets to its Tally inventory robots fleet in 2021','Its ESG report records Tally inventory robots being introduced to 11 more UAE Carrefour stores in 2021'),
('2022 p. 44','2022, p. 44'),
('Based on the existing service blueprint of a typical physical grocery store, as shown in Figure 1, the following is an improved service blueprint for a physical grocery store, from planning a basket all the way to postpurchase issues.','Figure 1 shows our proposed improved blueprint for a physical grocery store, from planning a basket to dealing with problems after purchase.')],
7:[
("What we're measuring for automation is the effort that's saving the shopper.","What we're measuring is how much effort automation saves the shopper."),
('The use of accurate shelf alerts is only useful if someone does something as a result.','Accurate shelf alerts are useful only if someone acts on them.'),
("When a receipt error is a problem, fast checkout isn't as useful.","When receipt errors are hard to fix, fast checkout isn't as useful.")],
9:[
('Huang and Rust (2021) identify three types of AI: Mechanical, Thinking, and Feeling.','Huang and Rust (2021) identify mechanical AI for repetitive tasks, thinking AI for analysis, and feeling AI for interpreting emotions.'),
('Repetitive scanning of shelves falls mainly into the first type, the recognition of missing items and the recommendation of alternatives into the analytical processing.','Shelf scanning mainly fits the first type; recognizing missing items and recommending alternatives require analysis.'),
('A barcode scanner is an SST, not an AI.','A barcode scanner is self-service technology, not necessarily AI.'),
('It is important not to overstate the benefits of AI and overlook the benefits of traditional automation.',"We shouldn't overstate AI's benefits or overlook traditional automation.")],
10:[
('which is carried through aisles','which moves through aisles'),
('The Majid Al Futtaim report provides information on missing items, misplaced items and incorrectly priced items.','The Majid Al Futtaim report describes checks for missing, misplaced and incorrectly priced items.'),
("A chatbot doesn't restock shelves, it processes information.","A chatbot doesn't restock shelves; it processes information."),
('resolves fail point F2: Recorded','addresses fail point F2: recorded')],
11:[
('in other countries in the UAE','in countries outside the UAE'),
('In June 2023 it said it was introducing a feature called Hopla on its French website that gives shoppers ideas on how to buy food according to their budget and dietary requirements (Carrefour, 2023).','In June 2023, it introduced Hopla on its French website, giving shoppers ideas based on their budget and dietary requirements (Carrefour, 2023).'),
("In June 2021, Brazil's Nutri Choice announced an algorithm to compare nutritional scores and prices, based on purchase history (Carrefour, 2021).","In June 2021, Carrefour announced Brazil's Nutri Choice, an algorithm comparing nutritional scores and prices using purchase history (Carrefour, 2021)."),
('Both are non-committal as far as UAE deployments go.','Neither announcement confirms a UAE deployment.'),
('Recommendations should be based on local catalog information and should include a statement giving the rationale for the recommendations; nutritional ratings may not be used instead of checking the ingredients.','Recommendations should use local catalog information and explain their rationale; nutritional ratings should not replace checking ingredients.')],
12:[
('Their system enables automated periodic checks and still includes staff for disputes.','Their framework supports automated checks while retaining staff for disputes.'),
('These conceptual predictions are not local customer acceptance.',"These predictions don't establish local customer acceptance."),
('Company publications also provide information on actions in lieu of independent satisfaction assessments.','Company publications describe initiatives, not independent satisfaction tests.'),
('Prior to scaling up the proposed system, Carrefour UAE must first assess task performance and customer effort.','Before scaling up, Carrefour UAE should assess task performance and customer effort.'),
("Carrefour's examples go further than automation to conversational advice.","Carrefour's examples extend automation to conversational advice."),
('In a bakery study, the recommendation effects were found to be different depending on the frequency of the visit (Song et al., 2024).','In a bakery study, recommendation effects varied with visit frequency (Song et al., 2024).'),
('It is a remotely controlled robot, which makes inferences about autonomous performance limited.','Its remotely controlled robot limits conclusions about autonomous performance.')],
14:[
('In stage 1, customers can benefit from recommendations that are both within their budget and take into account the size of packages and their current price.','In stage 1, customers can benefit from recommendations within their budget while still checking package sizes and current prices.'),
('In Fail point F1, the persuasiveness of advice leads to expectations that cannot be fulfilled by the store.','At fail point F1, persuasive advice can create expectations the store cannot meet.'),
('Include uncertainty information (such as source and update time) to enable consumers to evaluate uncertainty prior to their visit.','Showing the source and update time helps customers judge uncertainty before visiting.'),
('We feel it is better to warn of possible unavailability rather than to guarantee it.','We feel it is better to warn of possible unavailability than promise that an item is in stock.')],
15:[
('Even with assistive products','Even with digital tools'),
('This customer as co-producer approach is one of the reasons for the so-called "co-production" effect, which means that tasks may be outsourced to customers, but labor costs may be lowered due to the increased work required from customers (Wirtz, 2023).','The customer as co-producer approach explains how moving tasks to shoppers may lower labor costs while increasing customer work (Wirtz, 2023).'),
('If it was more time-consuming to register, as an alternative, there would be a search screen.','A search screen helps if using it takes less time than asking an employee.'),
('The second stage is thus made to maintain a route without the use of an application.','Stage 2 therefore keeps a route without an app.')],
17:[
('A customer can choose something','A customer can reject something'),
('With self check-out, the shopper is on his own in scanning items and checking the total.','With self-checkout, the shopper is responsible for scanning items and checking the total.'),
('If a price is not given at F4, then the price should be checked and the basket saved to avoid restarting by the shopper.','If a discount is missing at F4, staff should check the price and save the basket so the shopper need not restart.')],
18:[
('Once purchased, we would judge the retailer partially on how easily they are able to correct errors.','After purchase, we would judge the retailer partly on how easily it corrects errors.'),
('This is based on the principle for course process redesign proposed in the course, which emphasizes the elimination of steps in the process and the inclusion of recovery measures in case of self-service failure (Wirtz, 2023).',"This follows the course's process-redesign principle: remove unnecessary steps and provide recovery if self-service fails (Wirtz, 2023).")],
25:[
('Before implementing additional automation that reaches more customers','Before adding more customer-facing automation'),
('four week pilot','four-week pilot'),
('Expansion should be at no increased cost or complaint, but as better availability.','Expansion should improve availability without increasing complaints or staff workload.'),
('how many shelves are available','whether products are available on the shelves'),
('Close the alert at F2 after staff have established that the shelf is safe.','Close the alert at F2 only after staff confirm the item is available on the shelf.'),
('following safety incident','following a safety incident')],
26:[
('Track budget adherence, non-compliance and task completion, such as customers requiring staff support.','Track budget adherence, unsupported recommendations and task completion, including customers using staff support.'),
('Maintain the same service and service levels on routes.','Maintain the same offers and service levels across routes.'),
("If the catalog data can't give the advice, display doubt and provide staff assistance.","If catalog data can't support the advice, show uncertainty and provide staff assistance.")],
}
# Preserve the proposed response targets while correcting agreement and a run-on sentence.
changes[27]=[
('include customer verification before making changes','get customer confirmation before making changes'),
('Acknowledgment within 2 minutes after an in-store help request is made, and a human response within 1 working day of a post purchase case is proposed as pilot standards.','Proposed pilot standards are acknowledgment within 2 minutes of an in-store help request and a human response within 1 working day of a post-purchase case.'),
('Monitor the percentage of contacts that meet the standards, those that repeat and the amount of time that is taken to resolve the contacts these are targets and not measured outcomes.','Monitor the percentage meeting these standards, repeat contacts and total resolution time. These are targets, not measured outcomes.')]
changes[25].append(('Determine how accurately alerts are made and how long it takes until a verified shelf correction, and whether products are available on the shelves, compared to manual checking over similar trading times.','Compare alert accuracy, time to verified shelf correction and product availability with manual checking over similar trading times.'))
changes[28]=[("We would assess Carrefour's smart service based on the accuracy of the information and the ease of access for shoppers to get in touch with someone for assistance.","We would assess Carrefour's smart service by its information accuracy and how easily shoppers can get help.")]
result=[]
for i,pairs in changes.items():
 old=d.paragraphs[i].text;new=old
 for a,b in pairs:
  assert new.count(a)==1,(i,a)
  new=new.replace(a,b)
 result.append({'paragraph':i,'before':old,'after':new,'replacements':pairs})
text=[p.text for p in d.paragraphs]
for c in result:text[c['paragraph']]=c['after']
fig=next(i for i,t in enumerate(text) if t.startswith('Figure 1 Proposed'))
main='\n'.join(text[:fig]);total=len(main.split())+375
(R/'Source/edits.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('MAIN',len(main.split()),'TOTAL',total,'CUT',2168-total)
