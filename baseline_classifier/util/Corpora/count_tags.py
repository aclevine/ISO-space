import mae_corpus

# Ride for Climate
rfc_corpus_directory = '/Users/zach/Dropbox/ISO-Space/Annotation/RFC/Adjudication/Fix-up/rfc_BB_review_11-17-13/xmls/'

rfc_corpus_files = ["Amazon-BB-review.xml", "Andes-BB-review.xml", "Argentina-BB-review.xml", "Bicycles-BB-review.xml", "Bogota-BB-review.xml", "BuenosAires-BB-review.xml", "Cartagena-BB-review.xml", "Colon-BB-review.xml", "Copala-BB-review.xml", "Cusco-BB-review.xml", "Durango-BB-review.xml", "Ensenada-BB-review.xml", "Floods-BB-review.xml", "Glaciers-BB-review.xml", "Guatemala-BB-review.xml", "GuerreroNegro-BB-review.xml", "Hollywood-BB-review.xml", "Honduras-BB-review.xml", "HorseAssisted-BB-review.xml", "Huaraz-BB-review.xml", "Hurricanes-BB-review.xml", "IntoTheAndes-BB-review.xml", "LaPaz-BB-review.xml", "Lima-BB-review.xml", "Loreto-BB-review.xml", "LosAngeles-BB-review.xml", "MachuPicho-BB-review.xml", "Manaus-BB-review.xml", "Mazatlan-BB-review.xml", "Medellin-BB-review.xml", "MexicoCity-BB-review.xml", "Monarchs-BB-review.xml", "Oceans-BB-review.xml", "Paramo-BB-review.xml", "Peru-BB-review.xml", "PublicSchools-BB-review.xml", "PuertoOrdaz-BB-review.xml", "Queretaro-BB-review.xml", "RideForClimateUSA-BB-review.xml", "SanDiego-BB-review.xml", "SanPedroSula-BB-review.xml", "Tikal-BB-review.xml", "Transportation-BB-review.xml", "Update-BB-review.xml", "Yurimaguas-BB-review.xml"]

rfc_corpus = mae_corpus.Corpus(rfc_corpus_directory, rfc_corpus_files)

# Confluence Project
cp_corpus_directory = '/Users/zach/Dropbox/ISO-Space/Annotation/CP/Benjamin Beaudett/'

cp_corpus_files = ["45_N_22_E-BB-p4.xml", "45_N_23_E-BB-p4.xml", "46_N_21_E-BB-p4.xml", "46_N_22_E-BB-p4.xml", "46_N_23_E-BB-p4.xml", "46_N_24_E-BB-p4.xml", "46_N_25_E-BB-p4.xml", "46_N_26_E-BB-p4.xml", "46_N_27_E-BB-p4.xml", "46_N_28_E-BB-p4.xml", "47_N_23_E-BB-p4.xml", "47_N_24_E-BB-p4.xml", "47_N_25_E-BB-p4.xml", "47_N_26_E-BB-p4.xml", "47_N_27_E-BB-p4.xml", "47_N_28_E-BB-p4.xml", "48_N_10_E-BB-p4.xml", "48_N_11_E-BB-p4.xml", "48_N_12_E-BB-p4.xml", "48_N_27_E-BB-p4.xml", "48_N_8_E-BB-p4.xml"]

cp_corpus = mae_corpus.Corpus(cp_corpus_directory, cp_corpus_files)

# CLEF

clef_corpus_directory = '/Users/zach/Dropbox/ISO-Space/Annotation/IAPRTC/Adjudication/A10/'

clef_corpus_files = ["2007-A10-p2.eng.xml", "2008-A10-p2.eng.xml", "2009-A10-p2.eng.xml", "2010-A10-p2.eng.xml", "2012-A10-p2.eng.xml", "2014-A10-p2.eng.xml", "2015-A10-p2.eng.xml", "2017-A10-p2.eng.xml", "2018-A10-p2.eng.xml", "2020-A10-p2.eng.xml", "2022-A10-p2.eng.xml", "2023-A10-p2.eng.xml", "2024-A10-p2.eng.xml", "2025-A10-p2.eng.xml", "2027-A10-p2.eng.xml", "2029-A10-p2.eng.xml", "2032-A10-p2.eng.xml", "2033-A10-p2.eng.xml", "2034-A10-p2.eng.xml", "2037-A10-p2.eng.xml", "2039-A10-p2.eng.xml", "2040-A10-p2.eng.xml", "2042-A10-p2.eng.xml", "2043-A10-p2.eng.xml", "2044-A10-p2.eng.xml", "2047-A10-p2.eng.xml", "2049-A10-p2.eng.xml", "2050-A10-p2.eng.xml", "2052-A10-p2.eng.xml", "2053-A10-p2.eng.xml", "2054-A10-p2.eng.xml", "2055-A10-p2.eng.xml", "2058-A10-p2.eng.xml", "2059-A10-p2.eng.xml", "2063-A10-p2.eng.xml", "2065-A10-p2.eng.xml", "2067-A10-p2.eng.xml", "2068-A10-p2.eng.xml", "2070-A10-p2.eng.xml", "2072-A10-p2.eng.xml", "2073-A10-p2.eng.xml", "2074-A10-p2.eng.xml", "2077-A10-p2.eng.xml", "2078-A10-p2.eng.xml", "2079-A10-p2.eng.xml", "2080-A10-p2.eng.xml", "2082-A10-p2.eng.xml", "2083-A10-p2.eng.xml", "2084-A10-p2.eng.xml", "2085-A10-p2.eng.xml", "2087-A10-p2.eng.xml", "2089-A10-p2.eng.xml", "2090-A10-p2.eng.xml", "2092-A10-p2.eng.xml", "2093-A10-p2.eng.xml", "2094-A10-p2.eng.xml", "2095-A10-p2.eng.xml", "2097-A10-p2.eng.xml", "2098-A10-p2.eng.xml", "2099-A10-p2.eng.xml", "2100-A10-p2.eng.xml", "2102-A10-p2.eng.xml", "2104-A10-p2.eng.xml", "2107-A10-p2.eng.xml", "2108-A10-p2.eng.xml", "2109-A10-p2.eng.xml", "2110-A10-p2.eng.xml", "2112-A10-p2.eng.xml", "2113-A10-p2.eng.xml", "2114-A10-p2.eng.xml", "2117-A10-p2.eng.xml", "2118-A10-p2.eng.xml", "2119-A10-p2.eng.xml", "2120-A10-p2.eng.xml", "2122-A10-p2.eng.xml", "2124-A10-p2.eng.xml", "2129-A10-p2.eng.xml", "2133-A10-p2.eng.xml", "2138-A10-p2.eng.xml", "2139-A10-p2.eng.xml", "2140-A10-p2.eng.xml", "2142-A10-p2.eng.xml", "2144-A10-p2.eng.xml", "2145-A10-p2.eng.xml", "2147-A10-p2.eng.xml", "2148-A10-p2.eng.xml", "2149-A10-p2.eng.xml", "2150-A10-p2.eng.xml", "2152-A10-p2.eng.xml", "2153-A10-p2.eng.xml", "2155-A10-p2.eng.xml", "2157-A10-p2.eng.xml", "2158-A10-p2.eng.xml", "2159-A10-p2.eng.xml", "2160-A10-p2.eng.xml", "2162-A10-p2.eng.xml", "2163-A10-p2.eng.xml", "2164-A10-p2.eng.xml", "2165-A10-p2.eng.xml", "2167-A10-p2.eng.xml", "2168-A10-p2.eng.xml", "2169-A10-p2.eng.xml", "2170-A10-p2.eng.xml", "2172-A10-p2.eng.xml", "2173-A10-p2.eng.xml", "2175-A10-p2.eng.xml", "2177-A10-p2.eng.xml", "2178-A10-p2.eng.xml", "2179-A10-p2.eng.xml", "2180-A10-p2.eng.xml", "2182-A10-p2.eng.xml", "2183-A10-p2.eng.xml", "2184-A10-p2.eng.xml", "2188-A10-p2.eng.xml", "2189-A10-p2.eng.xml", "2192-A10-p2.eng.xml", "2193-A10-p2.eng.xml", "2194-A10-p2.eng.xml", "2195-A10-p2.eng.xml", "2197-A10-p2.eng.xml", "2199-A10-p2.eng.xml", "2202-A10-p2.eng.xml", "2203-A10-p2.eng.xml", "2204-A10-p2.eng.xml", "2205-A10-p2.eng.xml", "2207-A10-p2.eng.xml", "2208-A10-p2.eng.xml", "2209-A10-p2.eng.xml", "2210-A10-p2.eng.xml", "2212-A10-p2.eng.xml", "2213-A10-p2.eng.xml", "2215-A10-p2.eng.xml", "2217-A10-p2.eng.xml", "2218-A10-p2.eng.xml", "2219-A10-p2.eng.xml", "2220-A10-p2.eng.xml", "2222-A10-p2.eng.xml", "2223-A10-p2.eng.xml", "2224-A10-p2.eng.xml", "2225-A10-p2.eng.xml", "2228-A10-p2.eng.xml", "2229-A10-p2.eng.xml", "2230-A10-p2.eng.xml", "2232-A10-p2.eng.xml", "2233-A10-p2.eng.xml", "2235-A10-p2.eng.xml", "2237-A10-p2.eng.xml", "2238-A10-p2.eng.xml", "2239-A10-p2.eng.xml", "2240-A10-p2.eng.xml", "2242-A10-p2.eng.xml", "2244-A10-p2.eng.xml", "2245-A10-p2.eng.xml", "2247-A10-p2.eng.xml", "2248-A10-p2.eng.xml", "2250-A10-p2.eng.xml", "2253-A10-p2.eng.xml", "2254-A10-p2.eng.xml", "2255-A10-p2.eng.xml", "2257-A10-p2.eng.xml", "2258-A10-p2.eng.xml", "2259-A10-p2.eng.xml", "2260-A10-p2.eng.xml", "2262-A10-p2.eng.xml", "2263-A10-p2.eng.xml", "2264-A10-p2.eng.xml", "2265-A10-p2.eng.xml", "2267-A10-p2.eng.xml", "2268-A10-p2.eng.xml", "2269-A10-p2.eng.xml", "2270-A10-p2.eng.xml", "2272-A10-p2.eng.xml", "2273-A10-p2.eng.xml", "2274-A10-p2.eng.xml", "2275-A10-p2.eng.xml", "2277-A10-p2.eng.xml", "2278-A10-p2.eng.xml", "2280-A10-p2.eng.xml", "2282-A10-p2.eng.xml", "2283-A10-p2.eng.xml", "2284-A10-p2.eng.xml", "2285-A10-p2.eng.xml", "2287-A10-p2.eng.xml", "2288-A10-p2.eng.xml", "2289-A10-p2.eng.xml", "2290-A10-p2.eng.xml", "2292-A10-p2.eng.xml", "2294-A10-p2.eng.xml", "2636-A10-p2.eng.xml", "2641-A10-p2.eng.xml", "2643-A10-p2.eng.xml", "2645-A10-p2.eng.xml", "2651-A10-p2.eng.xml", "2652-A10-p2.eng.xml", "2653-A10-p2.eng.xml", "2655-A10-p2.eng.xml", "2656-A10-p2.eng.xml", "2657-A10-p2.eng.xml", "2658-A10-p2.eng.xml", "2660-A10-p2.eng.xml", "2661-A10-p2.eng.xml", "2662-A10-p2.eng.xml", "2663-A10-p2.eng.xml", "2666-A10-p2.eng.xml", "2668-A10-p2.eng.xml", "2671-A10-p2.eng.xml", "2672-A10-p2.eng.xml", "2675-A10-p2.eng.xml", "2676-A10-p2.eng.xml", "2677-A10-p2.eng.xml", "2678-A10-p2.eng.xml", "2680-A10-p2.eng.xml", "2682-A10-p2.eng.xml", "2685-A10-p2.eng.xml", "2687-A10-p2.eng.xml", "2688-A10-p2.eng.xml", "2690-A10-p2.eng.xml", "2691-A10-p2.eng.xml", "2692-A10-p2.eng.xml", "2693-A10-p2.eng.xml", "2695-A10-p2.eng.xml", "2696-A10-p2.eng.xml", "2697-A10-p2.eng.xml", "2699-A10-p2.eng.xml", "2701-A10-p2.eng.xml", "2702-A10-p2.eng.xml", "2705-A10-p2.eng.xml", "2707-A10-p2.eng.xml", "2710-A10-p2.eng.xml", "2711-A10-p2.eng.xml", "2712-A10-p2.eng.xml", "2714-A10-p2.eng.xml", "2715-A10-p2.eng.xml", "2716-A10-p2.eng.xml", "2717-A10-p2.eng.xml", "2719-A10-p2.eng.xml", "2720-A10-p2.eng.xml", "2724-A10-p2.eng.xml", "2725-A10-p2.eng.xml", "2726-A10-p2.eng.xml", "2729-A10-p2.eng.xml", "2731-A10-p2.eng.xml", "2734-A10-p2.eng.xml", "2741-A10-p2.eng.xml", "2743-A10-p2.eng.xml", "2745-A10-p2.eng.xml", "2746-A10-p2.eng.xml", "2764-A10-p2.eng.xml", "2765-A10-p2.eng.xml", "2766-A10-p2.eng.xml", "2768-A10-p2.eng.xml", "2769-A10-p2.eng.xml", "2770-A10-p2.eng.xml", "2771-A10-p2.eng.xml", "2773-A10-p2.eng.xml", "2774-A10-p2.eng.xml", "2775-A10-p2.eng.xml", "2776-A10-p2.eng.xml", "2778-A10-p2.eng.xml", "2779-A10-p2.eng.xml", "2780-A10-p2.eng.xml", "2783-A10-p2.eng.xml", "2784-A10-p2.eng.xml", "2785-A10-p2.eng.xml", "2786-A10-p2.eng.xml", "2788-A10-p2.eng.xml", "2789-A10-p2.eng.xml", "2790-A10-p2.eng.xml", "2791-A10-p2.eng.xml", "2793-A10-p2.eng.xml", "2794-A10-p2.eng.xml", "2795-A10-p2.eng.xml", "2796-A10-p2.eng.xml", "2798-A10-p2.eng.xml", "2799-A10-p2.eng.xml", "2800-A10-p2.eng.xml", "2804-A10-p2.eng.xml", "2805-A10-p2.eng.xml", "2807-A10-p2.eng.xml", "2808-A10-p2.eng.xml", "2809-A10-p2.eng.xml", "2810-A10-p2.eng.xml", "2813-A10-p2.eng.xml", "2814-A10-p2.eng.xml", "2818-A10-p2.eng.xml", "2819-A10-p2.eng.xml", "2826-A10-p2.eng.xml", "2827-A10-p2.eng.xml", "2828-A10-p2.eng.xml", "2829-A10-p2.eng.xml", "2831-A10-p2.eng.xml", "2832-A10-p2.eng.xml", "2833-A10-p2.eng.xml", "2834-A10-p2.eng.xml", "2836-A10-p2.eng.xml", "2837-A10-p2.eng.xml", "2838-A10-p2.eng.xml", "2839-A10-p2.eng.xml", "2841-A10-p2.eng.xml", "2842-A10-p2.eng.xml", "2843-A10-p2.eng.xml", "2844-A10-p2.eng.xml", "2846-A10-p2.eng.xml", "2847-A10-p2.eng.xml", "2848-A10-p2.eng.xml", "2849-A10-p2.eng.xml", "2851-A10-p2.eng.xml", "2852-A10-p2.eng.xml", "2853-A10-p2.eng.xml", "2854-A10-p2.eng.xml", "2856-A10-p2.eng.xml", "2857-A10-p2.eng.xml", "2858-A10-p2.eng.xml", "2859-A10-p2.eng.xml", "2861-A10-p2.eng.xml", "2864-A10-p2.eng.xml", "2866-A10-p2.eng.xml", "2867-A10-p2.eng.xml", "2868-A10-p2.eng.xml", "2872-A10-p2.eng.xml", "2874-A10-p2.eng.xml", "2877-A10-p2.eng.xml", "2879-A10-p2.eng.xml", "2882-A10-p2.eng.xml", "2883-A10-p2.eng.xml", "2884-A10-p2.eng.xml", "2886-A10-p2.eng.xml", "2887-A10-p2.eng.xml", "2888-A10-p2.eng.xml", "2889-A10-p2.eng.xml", "2891-A10-p2.eng.xml", "2897-A10-p2.eng.xml", "2898-A10-p2.eng.xml", "2901-A10-p2.eng.xml", "2902-A10-p2.eng.xml", "2903-A10-p2.eng.xml", "2907-A10-p2.eng.xml", "2908-A10-p2.eng.xml", "2909-A10-p2.eng.xml", "2911-A10-p2.eng.xml", "2913-A10-p2.eng.xml", "2916-A10-p2.eng.xml", "2917-A10-p2.eng.xml", "2918-A10-p2.eng.xml", "2919-A10-p2.eng.xml", "2921-A10-p2.eng.xml", "2922-A10-p2.eng.xml", "2923-A10-p2.eng.xml", "2924-A10-p2.eng.xml", "2926-A10-p2.eng.xml", "2927-A10-p2.eng.xml", "2928-A10-p2.eng.xml", "2929-A10-p2.eng.xml", "2932-A10-p2.eng.xml", "2933-A10-p2.eng.xml", "2934-A10-p2.eng.xml", "2936-A10-p2.eng.xml", "2937-A10-p2.eng.xml", "2938-A10-p2.eng.xml", "2939-A10-p2.eng.xml", "2941-A10-p2.eng.xml", "2942-A10-p2.eng.xml", "2943-A10-p2.eng.xml", "2944-A10-p2.eng.xml", "2946-A10-p2.eng.xml", "2947-A10-p2.eng.xml", "2948-A10-p2.eng.xml", "2949-A10-p2.eng.xml", "2951-A10-p2.eng.xml", "2952-A10-p2.eng.xml", "2953-A10-p2.eng.xml", "2954-A10-p2.eng.xml", "2956-A10-p2.eng.xml", "2957-A10-p2.eng.xml", "2958-A10-p2.eng.xml", "2959-A10-p2.eng.xml", "2961-A10-p2.eng.xml", "2962-A10-p2.eng.xml", "2963-A10-p2.eng.xml", "2964-A10-p2.eng.xml", "2966-A10-p2.eng.xml", "2967-A10-p2.eng.xml", "2968-A10-p2.eng.xml", "2969-A10-p2.eng.xml", "2971-A10-p2.eng.xml", "2972-A10-p2.eng.xml", "2973-A10-p2.eng.xml", "2974-A10-p2.eng.xml", "2976-A10-p2.eng.xml", "2977-A10-p2.eng.xml", "2978-A10-p2.eng.xml", "2979-A10-p2.eng.xml", "2981-A10-p2.eng.xml", "2982-A10-p2.eng.xml", "2983-A10-p2.eng.xml", "2984-A10-p2.eng.xml", "2986-A10-p2.eng.xml", "2987-A10-p2.eng.xml", "2988-A10-p2.eng.xml", "2989-A10-p2.eng.xml", "2991-A10-p2.eng.xml", "2992-A10-p2.eng.xml", "2993-A10-p2.eng.xml", "2994-A10-p2.eng.xml", "2996-A10-p2.eng.xml", "2997-A10-p2.eng.xml", "2998-A10-p2.eng.xml", "2999-A10-p2.eng.xml"]

clef_corpus = mae_corpus.Corpus(clef_corpus_directory, clef_corpus_files)


trial_directory = '/Users/zach/Dropbox/ISO-Space/SemEval/Trial/Final/'

trial_files = [
    "2008.xml",
    "2009.xml",
    "2010.xml",
    "2012.xml",
    "2014.xml",
    "2015.xml",
    "2017.xml",
    "2018.xml",
    "2020.xml",
    "45_N_22_E.xml",
    "46_N_26_E.xml",
    "46_N_27_E.xml",
    "47_N_22_E.xml",
    "47_N_23_E.xml",
    "47_N_25_E.xml",
    "Copala.xml",
    "Oceans.xml",
    "WhereToJapan-TheImperialPalace.xml",
    "WhereToJapan-Tokyo.xml",
    "WhereToJapan-WheretoGo.xml",
    "WhereToMadrid_BourbonMadrid.xml",
    "WhereToMadrid_NearthePuertadelSol.xml",
    "WhereToMadrid_WheretoGo.xml"
]


corpora = [("RFC", rfc_corpus), ("CP", cp_corpus), ("CLEF", clef_corpus)]

tag_set = [rfc_corpus.tag_types, cp_corpus.tag_types, clef_corpus.tag_types]

tag_types = set.union(*tag_set)

# tag_types_header = str([e.strip("'") for e in tag_types]).strip("[]").replace(",", "\t")


#    output = label + "\t"
#    for tag in tag_types:
#        datum = str(len(corpus.tag_dictionary[tag])) if tag in corpus.tag_dictionary.keys() else 0
#        output = output + "\t" + datum
#    output = output + "\n"
#    print output
print (" ", (['Sentences'] + list(tag_types)))

for (label, corpus) in corpora:
    data = []
    data.append(len(corpus.sentences))
    for tag in tag_types:
        datum = 0
        if tag in corpus.tag_dictionary.keys():
            datum = len(corpus.tag_dictionary[tag])
        data.append(datum)
    print (label, data)

# for (name, corpus) in corpora:
#    print name
#    corpus.tag_counts()
