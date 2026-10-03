"""
Disease information dictionary and helper functions for Plant Disease Detection.
Provides educational descriptions, symptom lists, and suggested management steps.
"""

# Educational and comprehensive disease knowledge base
DISEASE_INFO = {
    "Apple___Apple_scab": {
        "plant": "Apple",
        "disease": "Apple Scab (Venturia inaequalis)",
        "description": "Apple scab is a serious fungal disease affecting Malus species. It causes olive-green to black velvety spots on leaves and scabby lesions on fruit, leading to premature defoliation and unmarketable fruit.",
        "symptoms": [
            "Olive-green to dark brown velvety spots on upper leaf surfaces",
            "Yellowing and puckering around leaf lesions",
            "Premature leaf drop mid-season",
            "Corky, brown scab lesions on apple fruit surfaces"
        ],
        "treatment": [
            "Rake and destroy fallen leaves in autumn to eliminate overwintering fungal spores.",
            "Prune canopy during dormancy to promote air circulation and rapid leaf drying.",
            "Apply protective fungicides (captan, sulfur, or myclobutanil) starting at green tip stage.",
            "Select scab-resistant apple cultivars such as Liberty, Enterprise, or Freedom."
        ]
    },
    "Apple___Black_rot": {
        "plant": "Apple",
        "disease": "Black Rot (Botryosphaeria obtusa)",
        "description": "Black rot is a fungal pathogen causing leaf spot ('frog-eye' spots), cankers on branches, and rotting of fruit. The disease thrives in warm, humid weather.",
        "symptoms": [
            "Small purple specks on leaves expanding into circular 'frog-eye' lesions with tan centers",
            "Firm, concentric ring rot on mature apples turning pitch black",
            "Sunken reddish-brown cankers on twigs and main limbs",
            "Mummified fruit remaining clinging to branches through winter"
        ],
        "treatment": [
            "Prune out dead wood, cankers, and mummified fruit; burn or discard away from orchard.",
            "Maintain tree vigor through balanced fertilization and adequate watering.",
            "Apply copper-based sprays or captan during petal fall and early fruit development.",
            "Avoid mechanical damage to bark and fruit during maintenance."
        ]
    },
    "Apple___Cedar_apple_rust": {
        "plant": "Apple",
        "disease": "Cedar Apple Rust (Gymnosporangium juniperi-virginianae)",
        "description": "A heteroecious rust fungus requiring both apple trees and Eastern red cedar (Juniperus virginiana) to complete its complex two-year life cycle.",
        "symptoms": [
            "Bright orange-yellow circular spots on upper leaf surfaces in late spring",
            "Small black dots (pycnia) forming in the center of leaf lesions",
            "Tube-like fungal structures (aecia) on the underside of leaves shedding powdery spores",
            "Swollen rust spots on developing fruit causing distortion"
        ],
        "treatment": [
            "Remove nearby eastern red cedar and juniper trees within 1–2 miles if feasible.",
            "Remove cedar apple galls from ornamental junipers in late winter before spring rains.",
            "Apply preventative fungicides (myclobutanil, mancozeb) from pink bud stage through early summer.",
            "Plant resistant apple varieties like Redfree, Williams' Pride, or Dayton."
        ]
    },
    "Apple___healthy": {
        "plant": "Apple",
        "disease": "Healthy Plant (No Disease Detected)",
        "description": "The apple foliage displays vibrant green pigmentation, uniform surface texture, and standard cell turgidity with no signs of fungal, bacterial, or viral pathogens.",
        "symptoms": [
            "Clean, glossy, deep green leaf blades",
            "No necrotic lesions, chlorosis, or powdery mildew",
            "Uniform leaf margins without scorching or curling",
            "Normal vigorous stem growth and node development"
        ],
        "treatment": [
            "Continue routine balanced irrigation and seasonal fertilizer applications.",
            "Inspect regularly for early signs of aphids, mites, or leafhoppers.",
            "Ensure seasonal dormant pruning to maintain good sun exposure and air flow.",
            "Mulch tree base with organic compost while avoiding direct contact with the trunk bark."
        ]
    },
    "Corn___Common_rust": {
        "plant": "Corn (Maize)",
        "disease": "Common Rust (Puccinia sorghi)",
        "description": "A wind-borne fungal infection common in maize during cool, humid conditions. Pustules rupture the epidermis, reducing photosynthetic capacity and grain fill.",
        "symptoms": [
            "Golden-brown to cinnamon-brown powdery pustules on both leaf surfaces",
            "Elongated, oval pustules scattered across the upper and lower leaf canopy",
            "Chlorotic halos surrounding older pustules",
            "Premature leaf drying under severe disease pressure"
        ],
        "treatment": [
            "Plant rust-resistant maize hybrids with specific Rp resistance genes.",
            "Apply foliar fungicides (triazole or strobilurin classes) if rust appears before tasseling.",
            "Maintain optimal field drainage and plant spacing to reduce canopy humidity.",
            "Rotate crops annually to break local pathogen pressure."
        ]
    },
    "Corn___Northern_Leaf_Blight": {
        "plant": "Corn (Maize)",
        "disease": "Northern Leaf Blight (Exserohilum turcicum)",
        "description": "A serious foliar fungal disease causing large elliptical lesions that can coalesce and devastate photosynthetic foliage in corn fields.",
        "symptoms": [
            "Long, cigar-shaped grayish-green to tan lesions (1 to 6 inches long)",
            "Lesions running parallel to leaf veins",
            "Dark olive fungal sporulation in lesion centers during wet weather",
            "Extensive leaf blighting and premature plant senescence"
        ],
        "treatment": [
            "Use hybrids containing multi-race Ht resistance genes.",
            "Till corn residue into soil post-harvest to speed up decomposition of fungal spores.",
            "Rotate fields with non-host crops like soybeans or small grains.",
            "Apply labeled strobilurin or triazole fungicides early when lesions first appear on lower leaves."
        ]
    },
    "Corn___healthy": {
        "plant": "Corn (Maize)",
        "disease": "Healthy Plant (No Disease Detected)",
        "description": "Corn leaves display excellent vegetative health, strong venation, rich chlorophyll content, and no pathogenic lesions.",
        "symptoms": [
            "Uniform green leaf color from base to leaf tip",
            "Strong, upright leaf posture with intact leaf veins",
            "No rust pustules, blights, or insect bore holes",
            "Even plant height and sturdy stalk development"
        ],
        "treatment": [
            "Provide balanced nitrogen, phosphorus, and potassium according to soil test recommendations.",
            "Monitor soil moisture during critical pollination and silking stages.",
            "Practice scout-based integrated pest management throughout the growing season."
        ]
    },
    "Grape___Black_rot": {
        "plant": "Grape",
        "disease": "Grape Black Rot (Guignardia bidwellii)",
        "description": "A destructive fungal disease of grapes that attacks leaves, shoots, and fruit clusters. Berry infections lead to complete fruit mummification.",
        "symptoms": [
            "Small, reddish-brown circular spots on leaves with tiny black pycnidia in rings",
            "Dark sunken cankers on young canes and petiole stems",
            "Grapes turn brown, shrivel into hard, black, wrinkled mummies",
            "Severe yield loss in warm, rainy microclimates"
        ],
        "treatment": [
            "Prune out diseased canes and destroy all mummified grape clusters during winter.",
            "Train vines on trellis systems that maximize sunlight penetration and wind movement.",
            "Apply fungicides (myclobutanil, captan, or mancozeb) from early bud-break through veraison.",
            "Keep the vineyard floor clean of weed cover to accelerate canopy drying."
        ]
    },
    "Grape___healthy": {
        "plant": "Grape",
        "disease": "Healthy Plant (No Disease Detected)",
        "description": "The grapevine foliage shows robust vitality, intact lobed leaf architecture, healthy petioles, and no fungal sporulation.",
        "symptoms": [
            "Rich emerald foliage with smooth leaf texture",
            "No leaf spots, mildew coatings, or necrotic veins",
            "Healthy tendril elongation and cluster flowering",
            "Even shoot vigor along the cordon"
        ],
        "treatment": [
            "Maintain seasonal shoot thinning and canopy leaf pulling around cluster zones.",
            "Apply prophylactic organic sulfur sprays when ambient temperatures are below 85°F.",
            "Irrigate efficiently using drip lines to avoid wetting foliage."
        ]
    },
    "Potato___Early_blight": {
        "plant": "Potato",
        "disease": "Potato Early Blight (Alternaria solani)",
        "description": "A widespread fungal disease affecting solanaceous crops. It attacks older leaves first and progresses upward, drastically diminishing tuber yields.",
        "symptoms": [
            "Target-like spots with distinct concentric dark rings on older lower leaves",
            "Yellow chlorotic halos surrounding lesions",
            "Leaves turn brown, dry out, and drop prematurely",
            "Brown, sunken corky lesions on tuber skin surfaces"
        ],
        "treatment": [
            "Practice a minimum 3-year crop rotation with non-solanaceous crops.",
            "Ensure steady nitrogen and potassium nutrition to avoid plant stress.",
            "Water with drip irrigation early in the morning rather than overhead sprinklers.",
            "Apply preventative chlorothalonil, copper hydroxide, or azoxystrobin fungicides."
        ]
    },
    "Potato___Late_blight": {
        "plant": "Potato",
        "disease": "Potato Late Blight (Phytophthora infestans)",
        "description": "A devastating oomycete pathogen historically responsible for the Irish Potato Famine. It can destroy whole fields within days under cool, wet conditions.",
        "symptoms": [
            "Dark, water-soaked, irregularly shaped lesions on leaves and petioles",
            "White velvety fungal/oomycete mold on leaf undersides during moist conditions",
            "Rapid stem collapse and widespread foul-smelling foliage decay",
            "Reddish-brown granular rot penetrating into potato tuber flesh"
        ],
        "treatment": [
            "Plant only certified disease-free seed potatoes.",
            "Eliminate cull piles, volunteer potato plants, and solanaceous weeds.",
            "Apply protective fungicides (mancozeb, chlorothalonil, cymoxanil) before canopy closure.",
            "Kill vines 2 weeks prior to harvest to prevent tuber contamination during digging."
        ]
    },
    "Potato___healthy": {
        "plant": "Potato",
        "disease": "Healthy Plant (No Disease Detected)",
        "description": "Potato foliage demonstrates active photosynthesis, pristine compound leaves, firm stems, and no signs of bacterial wilt or blight.",
        "symptoms": [
            "Lush dark green compound leaves",
            "Uniform leaf margins without wilting or burning",
            "No concentric spots, water-soaking, or white molds",
            "Sturdy erect stems with healthy flowering clusters"
        ],
        "treatment": [
            "Hill up soil around potato roots to protect developing tubers from sun exposure.",
            "Maintain consistent soil moisture, providing 1–2 inches of water per week.",
            "Scout weekly for Colorado potato beetles and flea beetles."
        ]
    },
    "Tomato___Bacterial_spot": {
        "plant": "Tomato",
        "disease": "Bacterial Spot (Xanthomonas spp.)",
        "description": "A destructive bacterial disease that causes leaf defoliation, blossom drop, and scarred fruit, favored by warm temperatures and splashing rains.",
        "symptoms": [
            "Small, dark, greasy or water-soaked spots on leaves (often < 3mm)",
            "Centers of leaf spots dry and tear, leaving a ragged appearance",
            "Severe yellowing of affected leaves and heavy premature defoliation",
            "Raised, scab-like brown lesions on tomato fruits"
        ],
        "treatment": [
            "Use certified pathogen-free seeds and disease-tested transplants.",
            "Avoid overhead irrigation; use drip irrigation to prevent bacterial splash.",
            "Apply fixed copper sprays combined with mancozeb for improved bacterial control.",
            "Sanitize trellises, stakes, and pruning tools with a 10% bleach solution."
        ]
    },
    "Tomato___Early_blight": {
        "plant": "Tomato",
        "disease": "Early Blight (Alternaria linariae / Alternaria solani)",
        "description": "One of the most common tomato diseases worldwide. It manifests as distinctive concentric 'bullseye' target spots on foliage, stems, and fruit.",
        "symptoms": [
            "Concentric ring target patterns on older leaves near the base",
            "Pronounced yellow chlorotic halos encircling dark lesions",
            "Leaves turn yellow, wither, and die from ground up ('firing')",
            "Sunken dark leathery cankers on stems and fruit stem-end rot"
        ],
        "treatment": [
            "Prune bottom 12 inches of foliage to keep leaves off damp soil.",
            "Apply 2–3 inches of straw mulch around plant bases to prevent soil splash.",
            "Apply preventative copper, chlorothalonil, or bio-fungicide (Bacillus subtilis).",
            "Stake or cage indeterminate tomatoes to enhance air movement and drying."
        ]
    },
    "Tomato___Late_blight": {
        "plant": "Tomato",
        "disease": "Late Blight (Phytophthora infestans)",
        "description": "A rapid and aggressive water mold disease capable of destroying healthy tomato crops within a few days of cool, foggy, or wet weather.",
        "symptoms": [
            "Large, greasy, irregular gray-green to brown water-soaked blotches",
            "Delicate white cottony mold visible on leaf undersides in high humidity",
            "Stems develop dark greasy brown girdling lesions that cause collapse",
            "Firm, greasy, olive-brown blotches expanding over green tomato fruits"
        ],
        "treatment": [
            "Promptly remove and bag heavily infected plants; do not compost them.",
            "Ensure plants are spaced generously for maximum air ventilation.",
            "Spray protective copper fungicides or mandipropamid before wet spells.",
            "Plant resistant tomato cultivars such as Mountain Magic, Defiant, or Plum Regal."
        ]
    },
    "Tomato___Leaf_Mold": {
        "plant": "Tomato",
        "disease": "Leaf Mold (Passalora fulva)",
        "description": "A fungal disease predominantly affecting greenhouse and high-tunnel tomatoes where relative humidity exceeds 85%.",
        "symptoms": [
            "Pale green or pale yellow spots on upper leaf surfaces with indistinct borders",
            "Olive-green to velvety brown mold growth on the corresponding underside",
            "Leaves curl, turn brown, and drop prematurely without affecting fruit directly",
            "Reduced fruit yield and sunburned fruit due to canopy loss"
        ],
        "treatment": [
            "Increase greenhouse ventilation and run circulation fans continuously.",
            "Keep night-time temperatures warm enough to prevent condensation on foliage.",
            "Space plants adequately and prune suckers to promote internal airflow.",
            "Apply copper or sulfur fungicides at the first sign of lower leaf discoloration."
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "plant": "Tomato",
        "disease": "Septoria Leaf Spot (Septoria lycopersici)",
        "description": "A very common fungal disease of tomatoes causing innumerable small circular spots on lower leaves, leading to severe defoliation and sunscalded fruit.",
        "symptoms": [
            "Numerous small circular spots (1-3mm) with dark borders and grayish-white centers",
            "Tiny black specks (pycnidia) clearly visible inside lesion centers",
            "Heavily spotted leaves turn yellow, wither, curl, and drop off",
            "Progressive defoliation moving rapidly from base to top of plant"
        ],
        "treatment": [
            "Practice strict 2 to 3-year crop rotation away from solanaceous plants.",
            "Mulch soil surface thoroughly to block overwintering fungal spores.",
            "Water only at the root zone using drip irrigation.",
            "Spray chlorothalonil, copper, or mancozeb at 7-10 day intervals during wet periods."
        ]
    },
    "Tomato___Spider_mites": {
        "plant": "Tomato",
        "disease": "Two-Spotted Spider Mite (Tetranychus urticae)",
        "description": "Minute arachnid pests that pierce plant cell walls and suck out contents, causing severe stippling, chlorosis, and fine silken webbing under hot, dry conditions.",
        "symptoms": [
            "Fine yellow or white speckling/stippling on leaf tops",
            "Silky spider webs visible on leaf undersides and stem junctions",
            "Leaves turn bronze or yellow, become papery, and drop",
            "Stunted plant growth and reduced fruit quality"
        ],
        "treatment": [
            "Spray leaf undersides with strong streams of water to dislodge mites and webs.",
            "Apply insecticidal soap, neem oil, or horticultural oils covering all surfaces.",
            "Introduce beneficial predatory mites (Phytoseiulus persimilis).",
            "Avoid excessive synthetic pyrethroids which kill natural mite predators."
        ]
    },
    "Tomato___Target_Spot": {
        "plant": "Tomato",
        "disease": "Target Spot (Corynespora cassiicola)",
        "description": "Fungal pathogen attacking tomato foliage and fruit in tropical and sub-tropical conditions, creating pinprick lesions that expand with concentric zonation.",
        "symptoms": [
            "Small brown pinpoint spots with light green haloes expanding over time",
            "Concentric rings appearing within mature circular brown lesions",
            "Upper and lower leaves develop large necrotic blighted areas",
            "Depressed circular lesions with dark cracked margins on fruit"
        ],
        "treatment": [
            "Maintain wider row spacing to ensure foliage dries quickly after morning dew.",
            "Avoid overhead irrigation and keep field weed-free.",
            "Apply strobilurin or carboxamide fungicides labeled for target spot.",
            "Remove diseased crop debris immediately following the final harvest."
        ]
    },
    "Tomato___Yellow_Leaf_Curl_Virus": {
        "plant": "Tomato",
        "disease": "Yellow Leaf Curl Virus (TYLCV)",
        "description": "A devastating plant virus transmitted by the silverleaf whitefly (Bemisia tabaci). Infected young plants rarely produce marketable fruit.",
        "symptoms": [
            "Severe upward curling and cupping of leaf margins",
            "Distinct yellowing (chlorosis) along leaf edges and between veins",
            "Leaves become noticeably reduced in size and leathery in texture",
            "Extreme stunting of plant height and massive flower drop"
        ],
        "treatment": [
            "Cover young nursery beds with fine insect netting (50-mesh) to block whiteflies.",
            "Manage whitefly populations using yellow sticky traps and horticultural oils.",
            "Rogue out and destroy infected viral plants immediately upon discovery.",
            "Select TYLCV-resistant hybrid tomato varieties."
        ]
    },
    "Tomato___healthy": {
        "plant": "Tomato",
        "disease": "Healthy Plant (No Disease Detected)",
        "description": "The tomato foliage exhibits optimal health, balanced chlorophyll concentration, pristine glandular trichomes, and robust reproductive flowering.",
        "symptoms": [
            "Vibrant, dark green compound leaves with crisp edges",
            "Absence of spots, lesions, chlorosis, or wilting",
            "Sturdy main stem with active flowering trusses and fruit set",
            "Strong root anchorage and consistent apical growth"
        ],
        "treatment": [
            "Maintain consistent weekly watering (approx. 1.5 inches) to prevent blossom end rot.",
            "Apply balanced tomato fertilizer rich in calcium and micronutrients.",
            "Prune side suckers selectively to balance vegetative mass with fruit load.",
            "Mulch base with clean straw or wood chips to stabilize soil moisture."
        ]
    },
    "Pepper_bell___Bacterial_spot": {
        "plant": "Bell Pepper",
        "disease": "Bacterial Spot (Xanthomonas euvesicatoria)",
        "description": "Bacterial spot on bell peppers causes leaf lesions, extensive defoliation, and fruit blemishes that lead to sunscald and secondary fruit rots.",
        "symptoms": [
            "Small water-soaked or necrotic spots on leaves that turn brown",
            "Leaf yellowing followed by significant leaf drop",
            "Rough, raised, blister-like or crater-like scabs on pepper fruit",
            "Exposed fruit suffers from secondary heat damage and decay"
        ],
        "treatment": [
            "Use certified disease-free seeds treated with hot water or sodium hypochlorite.",
            "Apply copper bactericides tank-mixed with mancozeb to slow bacterial spread.",
            "Rotate crops away from peppers, tomatoes, and eggplants for at least 2 years.",
            "Avoid entering the field when foliage is wet from rain or dew."
        ]
    },
    "Pepper_bell___healthy": {
        "plant": "Bell Pepper",
        "disease": "Healthy Plant (No Disease Detected)",
        "description": "Bell pepper foliage is healthy, showing bright green glossy leaves, sturdy branch joints, and active fruit flowering.",
        "symptoms": [
            "Smooth, rich green, intact leaves without spotting",
            "Strong branching stems with no dark cankers",
            "Uniform fruit shape with firm, shiny epidermis",
            "Active white flower buds and vigorous growth nodes"
        ],
        "treatment": [
            "Provide regular irrigation to maintain evenly damp (not waterlogged) soil.",
            "Apply compost or balanced organic vegetable food at early flowering.",
            "Provide light support stakes to keep heavy pepper fruits off the soil."
        ]
    }
}

# Educational disclaimer added to all diagnosis results
DISCLAIMER_TEXT = (
    "Disclaimer: This prediction is generated by an artificial intelligence model "
    "for educational and preliminary informational purposes only. Plant disease diagnoses "
    "should be verified by a certified agronomist, plant pathologist, or local agricultural "
    "extension service before applying commercial chemical treatments."
)


def format_class_name(class_name: str) -> tuple[str, str]:
    """
    Converts a raw dataset class name like 'Tomato___Early_blight' or 'Apple_scab'
    into human-friendly (plant_name, disease_name) strings.
    """
    clean = class_name.strip()
    
    if "___" in clean:
        parts = clean.split("___", 1)
        plant_raw, disease_raw = parts[0], parts[1]
    elif "_" in clean:
        parts = clean.split("_", 1)
        plant_raw, disease_raw = parts[0], parts[1]
    elif "-" in clean:
        parts = clean.split("-", 1)
        plant_raw, disease_raw = parts[0], parts[1]
    else:
        plant_raw, disease_raw = clean, "Condition"
        
    plant = plant_raw.replace("_", " ").title().strip()
    disease = disease_raw.replace("_", " ").title().strip()
    
    # Specific cleanup for common strings
    if disease.lower() == "healthy":
        disease = "Healthy (No Disease Detected)"
        
    return plant, disease


def get_disease_details(class_name: str) -> dict:
    """
    Retrieves complete disease metadata for a given class name.
    If the class is not explicitly in the pre-populated DISEASE_INFO,
    it dynamically formats the class name and generates informative,
    context-aware symptoms, description, and treatment recommendations.
    """
    # 1. Exact match
    if class_name in DISEASE_INFO:
        info = dict(DISEASE_INFO[class_name])
        info["disclaimer"] = DISCLAIMER_TEXT
        return info

    # 2. Check for case-insensitive or normalized match
    for key, val in DISEASE_INFO.items():
        if key.lower() == class_name.lower():
            info = dict(val)
            info["disclaimer"] = DISCLAIMER_TEXT
            return info

    # 3. Dynamic fallback for any arbitrary new dataset class
    plant, disease = format_class_name(class_name)
    is_healthy = "healthy" in class_name.lower() or "healthy" in disease.lower()

    if is_healthy:
        description = (
            f"The analyzed foliage of {plant} shows typical healthy physiological characteristics. "
            "No macroscopic symptoms of fungal pathogens, bacterial lesions, or viral chlorosis "
            "were detected."
        )
        symptoms = [
            f"Uniform pigmentation and healthy color distribution across {plant} foliage",
            "Intact epidermal cell structure without spotting or necrosis",
            "Healthy leaf margins and vigorous petiole posture",
            "Normal developmental growth rate"
        ]
        treatment = [
            "Maintain optimal soil moisture and avoid excessive moisture fluctuations.",
            "Apply balanced fertilizer according to current crop growth stage.",
            "Continue periodic leaf scouting to detect any emerging pest pressures early."
        ]
    else:
        description = (
            f"The image indicates pathology characteristic of {disease} on {plant}. "
            "This condition affects foliar tissues and may compromise photosynthetic efficiency, "
            "canopy density, and overall crop yield if left unmanaged."
        )
        symptoms = [
            f"Abnormal discoloration or lesion development visible on the {plant} foliage",
            "Localized tissue necrosis, chlorotic halos, or surface stippling",
            "Potential premature withering or wilting of affected leaf sectors",
            "Interference with healthy leaf expansion and transpiration"
        ]
        treatment = [
            f"Isolate affected {plant} specimens or prune diseased foliage with sanitized tools.",
            "Improve field spacing and adjust irrigation practices to keep leaves dry.",
            "Collect and destroy fallen leaf debris to suppress pathogen reproduction.",
            "Consult a regional agricultural extension agent to verify the specific strain and identify approved treatments."
        ]

    return {
        "plant": plant,
        "disease": disease,
        "description": description,
        "symptoms": symptoms,
        "treatment": treatment,
        "disclaimer": DISCLAIMER_TEXT
    }
