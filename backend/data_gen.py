import pandas as pd
import numpy as np
import json

# List of symptoms
symptoms = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
    'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings',
    'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough',
    'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
    'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain',
    'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
    'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
    'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
    'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate',
    'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus',
    'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels',
    'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
    'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain',
    'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
    'foul_smell_of urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
    'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
    'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches',
    'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum',
    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
    'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf',
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
    'silver_like_dusting', 'small_dent_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
    'yellow_crust_ooze'
]

# Disease mapping (as before)
disease_symptoms = {
    'Fungal infection': ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches'],
    'Allergy': ['continuous_sneezing', 'shivering', 'chills', 'watering_from_eyes'],
    'GERD': ['stomach_pain', 'acidity', 'ulcers_on_tongue', 'vomiting', 'cough', 'chest_pain'],
    'Chronic cholestasis': ['itching', 'vomiting', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'yellowing_of_eyes'],
    'Drug Reaction': ['itching', 'skin_rash', 'stomach_pain', 'burning_micturition', 'spotting_ urination'],
    'Peptic ulcer diseae': ['vomiting', 'indigestion', 'loss_of_appetite', 'abdominal_pain', 'passage_of_gases', 'internal_itching'],
    'AIDS': ['muscle_wasting', 'patches_in_throat', 'high_fever', 'extra_marital_contacts'],
    'Diabetes': ['fatigue', 'weight_loss', 'restlessness', 'lethargy', 'irregular_sugar_level', 'blurred_and_distorted_vision', 'excessive_hunger', 'increased_appetite', 'polyuria'],
    'Gastroenteritis': ['vomiting', 'sunken_eyes', 'dehydration', 'diarrhoea'],
    'Bronchial Asthma': ['fatigue', 'cough', 'high_fever', 'breathlessness', 'family_history', 'mucoid_sputum'],
    'Hypertension': ['headache', 'chest_pain', 'dizziness', 'loss_of_balance', 'lack_of_concentration'],
    'Migraine': ['acidity', 'indigestion', 'headache', 'blurred_and_distorted_vision', 'excessive_hunger', 'stiff_neck', 'depression', 'irritability', 'visual_disturbances'],
    'Cervical spondylosis': ['back_pain', 'dizziness', 'loss_of_balance', 'neck_pain', 'weakness_in_limbs', 'neck_pain'],
    'Paralysis (brain hemorrhage)': ['vomiting', 'headache', 'weakness_of_one_body_side', 'altered_sensorium'],
    'Jaundice': ['itching', 'vomiting', 'fatigue', 'weight_loss', 'high_fever', 'yellowish_skin', 'dark_urine', 'abdominal_pain'],
    'Malaria': ['chills', 'vomiting', 'high_fever', 'sweating', 'headache', 'nausea', 'muscle_pain'],
    'Chicken pox': ['itching', 'skin_rash', 'fatigue', 'high_fever', 'headache', 'loss_of_appetite', 'mild_fever', 'swelled_lymph_nodes', 'malaise', 'red_spots_over_body'],
    'Dengue': ['skin_rash', 'chills', 'joint_pain', 'vomiting', 'fatigue', 'high_fever', 'headache', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'muscle_pain', 'red_spots_over_body'],
    'Typhoid': ['chills', 'vomiting', 'fatigue', 'high_fever', 'headache', 'nausea', 'constipation', 'abdominal_pain', 'diarrhoea', 'toxic_look_(typhos)', 'belly_pain'],
    'Hepatitis A': ['joint_pain', 'vomiting', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellowing_of_eyes'],
    'Hepatitis B': ['itching', 'fatigue', 'lethargy', 'yellowish_skin', 'dark_urine', 'loss_of_appetite', 'abdominal_pain', 'yellow_urine', 'yellowing_of_eyes', 'receiving_blood_transfusion', 'receiving_unsterile_injections'],
    'Hepatitis C': ['fatigue', 'yellowish_skin', 'nausea', 'loss_of_appetite', 'yellowing_of_eyes', 'family_history'],
    'Hepatitis D': ['joint_pain', 'vomiting', 'fatigue', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes'],
    'Hepatitis E': ['joint_pain', 'vomiting', 'fatigue', 'high_fever', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes', 'acute_liver_failure', 'coma', 'stomach_bleeding'],
    'Alcoholic hepatitis': ['vomiting', 'yellowish_skin', 'abdominal_pain', 'swelling_of_stomach', 'distention_of_abdomen', 'history_of_alcohol_consumption'],
    'Tuberculosis': ['chills', 'vomiting', 'fatigue', 'weight_loss', 'cough', 'high_fever', 'breathlessness', 'sweating', 'loss_of_appetite', 'mild_fever', 'phlegm', 'swelled_lymph_nodes', 'malaise', 'phlegm', 'chest_pain', 'blood_in_sputum'],
    'Common Cold': ['continuous_sneezing', 'chills', 'fatigue', 'cough', 'high_fever', 'headache', 'swelled_lymph_nodes', 'malaise', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'loss_of_smell', 'muscle_pain'],
    'Pneumonia': ['chills', 'fatigue', 'cough', 'high_fever', 'breathlessness', 'sweating', 'malaise', 'phlegm', 'chest_pain', 'fast_heart_rate', 'rusty_sputum'],
    'Dimorphic hemmorhoids(piles)': ['constipation', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus'],
    'Heart attack': ['vomiting', 'breathlessness', 'sweating', 'chest_pain'],
    'Varicose veins': ['fatigue', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'prominent_veins_on_calf'],
    'Hypothyroidism': ['fatigue', 'weight_gain', 'mood_swings', 'lethargy', 'dizziness', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'depression', 'irritability', 'abnormal_menstruation'],
    'Hyperthyroidism': ['fatigue', 'mood_swings', 'weight_loss', 'restlessness', 'sweating', 'diarrhoea', 'fast_heart_rate', 'excessive_hunger', 'muscle_weakness', 'irritability', 'abnormal_menstruation'],
    'Hypoglycemia': ['vomiting', 'fatigue', 'anxiety', 'sweating', 'headache', 'nausea', 'blurred_and_distorted_vision', 'excessive_hunger', 'drying_and_tingling_lips', 'slurred_speech', 'irritability', 'palpitations'],
    'Osteoarthristis': ['joint_pain', 'neck_pain', 'knee_pain', 'hip_joint_pain', 'swelling_joints', 'painful_walking'],
    'Arthritis': ['muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'painful_walking'],
    '(vertigo) Paroymsal Positional Vertigo': ['vomiting', 'headache', 'nausea', 'spinning_movements', 'loss_of_balance', 'unsteadiness'],
    'Acne': ['skin_rash', 'pus_filled_pimples', 'blackheads', 'scurring'],
    'Urinary tract infection': ['burning_micturition', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine'],
    'Psoriasis': ['skin_rash', 'joint_pain', 'skin_peeling', 'silver_like_dusting', 'small_dent_in_nails', 'inflammatory_nails'],
    'Impetigo': ['skin_rash', 'high_fever', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']
}

# Updated disease info with description, precautions and basic health tips
disease_info = {
    'Fungal infection': {
        'severity': 'Mild',
        'description': 'A fungal infection is a skin disease caused by a fungus. There are millions of species of fungi.',
        'precautions': ['Bath twice', 'Use dettol or neem in bathing water', 'Avoid sharing towels', 'Keep infected area dry'],
        'health_advice': 'Maintain high personal hygiene and wear breathable fabrics.'
    },
    'Allergy': {
        'severity': 'Mild',
        'description': 'An allergy is a reaction by your immune system to something that does not bother most other people.',
        'precautions': ['Avoid allergens', 'Use nasal spray', 'Stay indoors in high pollen', 'Take antihistamines'],
        'health_advice': 'Identify your triggers and keep emergency meds handy.'
    },
    'GERD': {
        'severity': 'Moderate',
        'description': 'Gastroesophageal reflux disease (GERD) is a digestive disorder that affects the ring of muscle between your esophagus and your stomach.',
        'precautions': ['Avoid fatty foods', 'Eat small meals', 'Don\'t lie down after eating', 'Maintain healthy weight'],
        'health_advice': 'Avoid late-night snacks and elevate your head while sleeping.'
    },
    'Chronic cholestasis': {
        'severity': 'High',
        'description': 'Chronic cholestasis is a condition where bile cannot flow from the liver to the duodenum.',
        'precautions': ['Consult a doctor', 'Avoid alcohol', 'Follow low fat diet', 'Eat more fiber'],
        'health_advice': 'Liver health is critical; prioritize a balanced, clean diet.'
    },
    'Drug Reaction': {
        'severity': 'High',
        'description': 'An adverse drug reaction (ADR) is an injury caused by taking medication.',
        'precautions': ['Stop taking the drug', 'Consult a doctor immediately', 'Note down the drug name', 'Drink plenty of water'],
        'health_advice': 'Always inform your doctor about your allergies before starting new medications.'
    },
    'Peptic ulcer diseae': {
        'severity': 'Moderate',
        'description': 'Peptic ulcers are open sores that develop on the inside lining of your stomach and the upper portion of your small intestine.',
        'precautions': ['Avoid spicy food', 'Drink cabbage juice', 'Eat small frequent meals', 'Reduce stress'],
        'health_advice': 'Avoid NSAIDs like aspirin unless prescribed by a doctor.'
    },
    'AIDS': {
        'severity': 'Critical',
        'description': 'Acquired immunodeficiency syndrome (AIDS) is a chronic, potentially life-threatening condition caused by the human immunodeficiency virus (HIV).',
        'precautions': ['Consult a specialist', 'Follow antiretroviral therapy', 'Use protection', 'Maintain healthy diet'],
        'health_advice': 'Consistency with medication and a strong support system are vital.'
    },
    'Diabetes': {
        'severity': 'High',
        'description': 'Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high.',
        'precautions': ['Monitor blood sugar', 'Regular exercise', 'Follow a diabetic diet', 'Stay hydrated'],
        'health_advice': 'Focus on whole grains and complex carbs. Avoid refined sugars.'
    },
    'Gastroenteritis': {
        'severity': 'Moderate',
        'description': 'Gastroenteritis is an inflammation of the lining of the intestines caused by a virus, bacteria, or parasites.',
        'precautions': ['Drink ORS', 'Eat bland food', 'Stay hydrated', 'Rest'],
        'health_advice': 'Wash hands frequently and ensure food is cooked thoroughly.'
    },
    'Bronchial Asthma': {
        'severity': 'High',
        'description': 'Asthma is a condition in which your airways narrow and swell and may produce extra mucus.',
        'precautions': ['Use inhaler', 'Avoid triggers', 'Breathing exercises', 'Consult doctor regularly'],
        'health_advice': 'Monitor air quality and avoid smoking areas.'
    },
    'Hypertension': {
        'severity': 'High',
        'description': 'Hypertension, also known as high blood pressure, is a long-term medical condition in which the blood pressure in the arteries is persistently elevated.',
        'precautions': ['Reduce salt intake', 'Regular exercise', 'Manage stress', 'Monitor blood pressure'],
        'health_advice': 'Adopt the DASH diet and engage in daily physical activity.'
    },
    'Migraine': {
        'severity': 'Moderate',
        'description': 'A migraine is a headache that can cause severe throbbing pain or a pulsing sensation, usually on one side of the head.',
        'precautions': ['Identify triggers', 'Rest in a dark room', 'Stay hydrated', 'Maintain sleep schedule'],
        'health_advice': 'Keep a migraine diary to track potential diet or environment triggers.'
    },
    'Cervical spondylosis': {
        'severity': 'Moderate',
        'description': 'Cervical spondylosis is a general term for age-related wear and tear affecting the spinal disks in your neck.',
        'precautions': ['Neck exercises', 'Use ergonomic furniture', 'Good posture', 'Heat/Cold therapy'],
        'health_advice': 'Take regular breaks from screen time and keep your neck aligned.'
    },
    'Paralysis (brain hemorrhage)': {
        'severity': 'Critical',
        'description': 'A brain hemorrhage is a type of stroke. It\'s caused by an artery in the brain bursting and causing localized bleeding in the surrounding tissues.',
        'precautions': ['Immediate emergency care', 'Rehabilitation therapy', 'Monitor blood pressure', 'Regular checkups'],
        'health_advice': 'Time is critical in stroke management; seek help immediately.'
    },
    'Jaundice': {
        'severity': 'High',
        'description': 'Jaundice is a condition in which the skin, whites of the eyes and mucous membranes turn yellow because of a high level of bilirubin.',
        'precautions': ['Rest', 'Drink plenty of fluids', 'Eat easily digestible food', 'Avoid alcohol'],
        'health_advice': 'Give your liver a break with a low-protein, high-fluid diet.'
    },
    'Malaria': {
        'severity': 'High',
        'description': 'Malaria is a disease caused by a parasite. The parasite is spread to humans through the bites of infected mosquitoes.',
        'precautions': ['Consult doctor', 'Complete medication course', 'Use mosquito nets', 'Keep surroundings clean'],
        'health_advice': 'Prevention is key; use repellents and sleep under nets in endemic areas.'
    },
    'Chicken pox': {
        'severity': 'Moderate',
        'description': 'Chickenpox is an infection caused by the varicella-zoster virus. It causes an itchy rash with small, fluid-filled blisters.',
        'precautions': ['Stay isolated', 'Avoid scratching blisters', 'Calamine lotion', 'Bathing in lukewarm water'],
        'health_advice': 'Vaccination can prevent most cases of chickenpox.'
    },
    'Dengue': {
        'severity': 'High',
        'description': 'Dengue fever is a mosquito-borne illness that occurs in tropical and subtropical areas of the world.',
        'precautions': ['Stay hydrated', 'Papaya leaf extract', 'Monitor platelet count', 'Use mosquito repellents'],
        'health_advice': 'Prevent mosquito breeding by ensuring no stagnant water around the house.'
    },
    'Typhoid': {
        'severity': 'High',
        'description': 'Typhoid fever is an infection caused by Salmonella typhi bacteria.',
        'precautions': ['Drink boiled water', 'Complete antibiotic course', 'Eat easily digestible food', 'Rest'],
        'health_advice': 'Avoid raw food and stick to hot, bottled water while traveling.'
    },
    'Hepatitis A': {
        'severity': 'Moderate',
        'description': 'Hepatitis A is a highly contagious liver infection caused by the hepatitis A virus.',
        'precautions': ['Rest', 'Avoid alcohol', 'Practice good hygiene', 'Small frequent meals'],
        'health_advice': 'Wash hands after using the bathroom and before handling food.'
    },
    'Hepatitis B': {
        'severity': 'High',
        'description': 'Hepatitis B is a serious liver infection caused by the hepatitis B virus (HBV).',
        'precautions': ['Consult specialist', 'Avoid sharing razors/needles', 'Healthy diet', 'Vaccination for family'],
        'health_advice': 'Regular screenings are important if you are at high risk.'
    },
    'Hepatitis C': {
        'severity': 'High',
        'description': 'Hepatitis C is a viral infection that causes liver inflammation, sometimes leading to serious liver damage.',
        'precautions': ['Consult specialist', 'Avoid alcohol', 'Healthy diet', 'Regular follow-up'],
        'health_advice': 'New treatments can cure most cases of Hepatitis C.'
    },
    'Hepatitis D': {
        'severity': 'High',
        'description': 'Hepatitis D, also known as the hepatitis delta virus, is an infection that causes inflammation of the liver.',
        'precautions': ['Consult specialist', 'Avoid alcohol', 'Healthy diet', 'Regular follow-up'],
        'health_advice': 'Hepatitis D only occurs in people who are also infected with Hepatitis B.'
    },
    'Hepatitis E': {
        'severity': 'High',
        'description': 'Hepatitis E is a liver inflammation caused by the hepatitis E virus (HEV).',
        'precautions': ['Consult specialist', 'Avoid alcohol', 'Clean water', 'Good hygiene'],
        'health_advice': 'Safety of water supply is the most effective way to prevent infection.'
    },
    'Alcoholic hepatitis': {
        'severity': 'High',
        'description': 'Alcoholic hepatitis is inflammation of the liver caused by drinking alcohol.',
        'precautions': ['Quit alcohol immediately', 'Consult doctor', 'Follow liver-friendly diet', 'Rest'],
        'health_advice': 'Complete abstinence from alcohol is the only way to halt liver damage.'
    },
    'Tuberculosis': {
        'severity': 'High',
        'description': 'Tuberculosis (TB) is a potentially serious infectious disease that mainly affects your lungs.',
        'precautions': ['Complete DOTS therapy', 'Wear a mask', 'High protein diet', 'Keep room ventilated'],
        'health_advice': 'Always finish your antibiotic course to prevent drug-resistant TB.'
    },
    'Common Cold': {
        'severity': 'Mild',
        'description': 'The common cold is a viral infection of your nose and throat (upper respiratory tract).',
        'precautions': ['Stay hydrated', 'Gargle with salt water', 'Steam inhalation', 'Vitamin C'],
        'health_advice': 'Rest is the best medicine for a common cold.'
    },
    'Pneumonia': {
        'severity': 'High',
        'description': 'Pneumonia is an infection that inflames the air sacs in one or both lungs.',
        'precautions': ['Antibiotics', 'Rest', 'Fluid intake', 'Breathing exercises'],
        'health_advice': 'Get the pneumonia vaccine if you are in a high-risk group.'
    },
    'Dimorphic hemmorhoids(piles)': {
        'severity': 'Moderate',
        'description': 'Hemorrhoids are swollen veins in your anus and lower rectum, similar to varicose veins.',
        'precautions': ['High fiber diet', 'Stay hydrated', 'Avoid straining', 'Warm baths'],
        'health_advice': 'Maintain a routine for bowel movements and drink 8 glasses of water daily.'
    },
    'Heart attack': {
        'severity': 'Critical',
        'description': 'A heart attack occurs when the flow of blood to the heart is severely reduced or blocked.',
        'precautions': ['Dial emergency immediately', 'Aspirin if advised', 'CPR training', 'Healthy lifestyle'],
        'health_advice': 'Know the warning signs and don\'t delay seeking help.'
    },
    'Varicose veins': {
        'severity': 'Moderate',
        'description': 'Varicose veins are twisted, enlarged veins.',
        'precautions': ['Compression stockings', 'Keep legs elevated', 'Exercise regularly', 'Avoid standing for long'],
        'health_advice': 'Avoid crossing your legs while sitting.'
    },
    'Hypothyroidism': {
        'severity': 'Moderate',
        'description': 'Hypothyroidism (underactive thyroid) is a condition in which your thyroid gland doesn\'t produce enough of certain crucial hormones.',
        'precautions': ['Thyroid medication', 'Iodine-rich diet', 'Monitor weight', 'Regular exercise'],
        'health_advice': 'Regular blood tests to check TSH levels are necessary.'
    },
    'Hyperthyroidism': {
        'severity': 'Moderate',
        'description': 'Hyperthyroidism (overactive thyroid) occurs when your thyroid gland produces too much of the hormone thyroxine.',
        'precautions': ['Consult specialist', 'Monitor heart rate', 'Low iodine diet', 'Manage stress'],
        'health_advice': 'Avoid caffeine as it can worsen symptoms like fast heart rate.'
    },
    'Hypoglycemia': {
        'severity': 'Moderate',
        'description': 'Hypoglycemia is a condition in which your blood sugar (glucose) level is lower than normal.',
        'precautions': ['Eat fast-acting sugar', 'Check blood glucose', 'Regular meals', 'Inform family/friends'],
        'health_advice': 'Always carry a source of sugar like hard candy or glucose tabs.'
    },
    'Osteoarthristis': {
        'severity': 'Moderate',
        'description': 'Osteoarthritis is the most common form of arthritis, affecting millions of people worldwide.',
        'precautions': ['Moderate exercise', 'Maintain weight', 'Physical therapy', 'Joint protection'],
        'health_advice': 'Swimming or cycling are great low-impact exercises for joints.'
    },
    'Arthritis': {
        'severity': 'Moderate',
        'description': 'Arthritis is the swelling and tenderness of one or more of your joints.',
        'precautions': ['Keep joints moving', 'Anti-inflammatory diet', 'Heat/Cold therapy', 'Consult specialist'],
        'health_advice': 'Omega-3 fatty acids found in fish oil can help reduce inflammation.'
    },
    '(vertigo) Paroymsal Positional Vertigo': {
        'severity': 'Moderate',
        'description': 'Benign paroxysmal positional vertigo (BPPV) is one of the most common causes of vertigo — the sudden sensation that you\'re spinning or that the inside of your head is spinning.',
        'precautions': ['Epley maneuver', 'Avoid sudden movements', 'Keep head elevated', 'Physical therapy'],
        'health_advice': 'Sit down immediately when you feel dizzy to prevent falls.'
    },
    'Acne': {
        'severity': 'Mild',
        'description': 'Acne is a skin condition that occurs when your hair follicles become plugged with oil and dead skin cells.',
        'precautions': ['Keep skin clean', 'Avoid touching face', 'Balanced diet', 'Consult dermatologist'],
        'health_advice': 'Don\'t pop pimples; it leads to scarring and more infection.'
    },
    'Urinary tract infection': {
        'severity': 'Moderate',
        'description': 'A urinary tract infection (UTI) is an infection in any part of your urinary system — your kidneys, ureters, bladder and urethra.',
        'precautions': ['Drink plenty of water', 'Cranberry juice', 'Vitamin C', 'Regular urination'],
        'health_advice': 'Wipe from front to back to prevent bacteria from entering the urethra.'
    },
    'Psoriasis': {
        'severity': 'Moderate',
        'description': 'Psoriasis is a skin disease that causes a rash with itchy, scaly patches, most commonly on the knees, elbows, trunk and scalp.',
        'precautions': ['Moisturize skin', 'Manage stress', 'Avoid triggers', 'UV light therapy'],
        'health_advice': 'Sunlight in moderation can help improve symptoms.'
    },
    'Impetigo': {
        'severity': 'Mild',
        'description': 'Impetigo is a highly contagious skin infection that mainly affects infants and children.',
        'precautions': ['Clean the area', 'Antibiotic cream', 'Avoid sharing items', 'Hand washing'],
        'health_advice': 'Keep fingernails short to prevent scratching the sores.'
    }
}

# Generate synthetic dataset as before
rows = []
for disease, syms in disease_symptoms.items():
    for _ in range(15): # More variations
        row = [0] * len(symptoms)
        count = np.random.randint(2, len(syms) + 1)
        selected = np.random.choice(syms, count, replace=False)
        for s in selected:
            row[symptoms.index(s)] = 1
        noise = np.random.choice(symptoms, 1)[0]
        if noise not in syms:
             row[symptoms.index(noise)] = 1
        row.append(disease)
        rows.append(row)

df = pd.DataFrame(rows, columns=symptoms + ['prognosis'])
df.to_csv('backend/data/symptoms_diseases.csv', index=False)

with open('backend/data/disease_info.json', 'w') as f:
    json.dump(disease_info, f)

print("Data generation complete with expanded metadata.")
