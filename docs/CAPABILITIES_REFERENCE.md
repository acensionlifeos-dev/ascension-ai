# Ascension AI - Complete Capability Reference

**Total capabilities:** 495

This is the single source of truth for the native capability surface. Each capability has a registered `id`, `name`, `category`, and `description`. The native chat router uses `id` to route to the matching handler in `src/services/native-domain-router.ts`.

| ID | Name | Category | Description |
|---|---|---|---|
| `audio_editing` | Audio Editing | audio | Edit and manipulate audio |
| `music_generation_suno` | Music Generation (Suno) | audio | Generate music with Suno AI |
| `music_generation_udio` | Music Generation (Udio) | audio | Generate music with Udio |
| `speech_to_text` | Speech-to-Text | audio | Convert speech to text with Whisper |
| `text_to_speech` | Text-to-Speech | audio | Convert text to speech with ElevenLabs |
| `voice_cloning` | Voice Cloning | audio | Clone voices with ElevenLabs |
| `ascension_bicycle` | Ascension Bicycle | automotive | Bicycle selection, maintenance, and riding |
| `ascension_boat` | Ascension Boat | automotive | Boating basics, safety, and maintenance |
| `ascension_car_buying` | Ascension Car Buying | automotive | Car buying, negotiation, and research |
| `ascension_car_maintenance` | Ascension Car Maintenance | automotive | Car maintenance, service schedules, and troubleshooting |
| `ascension_electric_vehicle` | Ascension Electric Vehicle | automotive | EV selection, charging, and ownership |
| `ascension_motorcycle` | Ascension Motorcycle | automotive | Motorcycle riding, gear, and maintenance |
| `ascension_rv` | Ascension RV | automotive | RV travel, maintenance, and trip planning |
| `ascension_affiliate` | Ascension Affiliate | business | Affiliate marketing, links, and commissions |
| `ascension_amazon` | Ascension Amazon | business | Amazon selling, FBA, and listings |
| `ascension_benefits` | Ascension Benefits | business | Employee benefits packages and selection |
| `ascension_brand` | Ascension Brand | business | Brand positioning, voice, and identity |
| `ascension_business_plan` | Ascension Business Plan | business | Business plan drafting and review |
| `ascension_chatbot` | Ascension Chatbot | business | Chatbot design, flows, and fallback |
| `ascension_churn` | Ascension Churn | business | Churn analysis and prevention |
| `ascension_compliance` | Ascension Compliance | business | Regulatory compliance, policies, and controls |
| `ascension_cross_sell` | Ascension Cross Sell | business | Cross-sell pairing and messaging |
| `ascension_crowdfunding` | Ascension Crowdfunding | business | Crowdfunding campaigns, rewards, and promotion |
| `ascension_customer_service` | Ascension Customer Service | business | Customer service, support, and retention |
| `ascension_customer_support` | Ascension Customer Support | business | Customer support, tickets, and responses |
| `ascension_dropshipping` | Ascension Dropshipping | business | Dropshipping suppliers, products, and risks |
| `ascension_ecommerce` | Ascension Ecommerce | business | Ecommerce strategy, platforms, and operations |
| `ascension_etsy` | Ascension Etsy | business | Etsy listings, SEO, and shop management |
| `ascension_export` | Ascension Export | business | Exporting goods, compliance, and markets |
| `ascension_faq` | Ascension FAQ | business | FAQ generation, maintenance, and answers |
| `ascension_fulfillment` | Ascension Fulfillment | business | Order fulfillment, 3PL, and warehousing |
| `ascension_fundraising` | Ascension Fundraising | business | Fundraising, investors, and grant seeking |
| `ascension_grants` | Ascension Grants | business | Grant research, applications, and reporting |
| `ascension_hr` | Ascension HR | business | Hiring, onboarding, and employee relations |
| `ascension_helpdesk` | Ascension Helpdesk | business | Helpdesk organization, priorities, and SLAs |
| `ascension_import` | Ascension Import | business | Importing goods, suppliers, and customs |
| `ascension_inventory` | Ascension Inventory | business | Inventory tracking, forecasting, and management |
| `ascension_knowledge_base` | Ascension Knowledge Base | business | Knowledge base articles, search, and updates |
| `ascension_live_chat` | Ascension Live Chat | business | Live chat scripts, routing, and handoff |
| `ascension_loyalty` | Ascension Loyalty | business | Loyalty programs, points, and rewards |
| `ascension_marketing` | Ascension Marketing | business | Marketing strategy, channels, and campaigns |
| `ascension_merchandise` | Ascension Merchandise | business | Merch design, production, and sales |
| `ascension_onboarding` | Ascension Onboarding | business | Customer and employee onboarding flows |
| `ascension_open_enrollment` | Ascension Open Enrollment | business | Open enrollment choices and deadlines |
| `ascension_pos` | Ascension POS | business | Point of sale systems and setup |
| `ascension_partnerships` | Ascension Partnerships | business | Partnership, alliance, and deal strategy |
| `ascension_patreon` | Ascension Patreon | business | Patreon tiers, rewards, and growth |
| `ascension_pitch` | Ascension Pitch | business | Pitch deck and investor presentation practice |
| `ascension_print_on_demand` | Ascension Print On Demand | business | Print on demand products and suppliers |
| `ascension_referral` | Ascension Referral | business | Referral program design and tracking |
| `ascension_reputation` | Ascension Reputation | business | Online reputation monitoring and response |
| `ascension_retention` | Ascension Retention | business | Customer retention strategies and signals |
| `ascension_sales` | Ascension Sales | business | Sales process, outreach, and closing |
| `ascension_shipping` | Ascension Shipping | business | Shipping carriers, rates, and packaging |
| `ascension_shopify` | Ascension Shopify | business | Shopify store setup, apps, and optimization |
| `ascension_sponsorships` | Ascension Sponsorships | business | Sponsorship outreach and deal terms |
| `ascension_startup` | Ascension Startup | business | Startup ideation, validation, and early operations |
| `ascension_tariffs` | Ascension Tariffs | business | Tariffs, duties, and trade compliance |
| `ascension_ticketing` | Ascension Ticketing | business | Ticket creation, routing, and resolution |
| `ascension_upsell` | Ascension Upsell | business | Upsell recommendations and timing |
| `ascension_woocommerce` | Ascension WooCommerce | business | WooCommerce setup, plugins, and payments |
| `ascension_workers_comp` | Ascension Workers Comp | business | Workers compensation basics and claims |
| `ascension_ebay` | Ascension eBay | business | eBay selling, auctions, and shipping |
| `business_growth` | Business Growth | business | Business growth strategies and intelligence |
| `ascension_career` | Ascension Career | career | Resume review, job matching, and career planning |
| `ascension_code` | Ascension Code | code | Code generation, review, debugging, and architecture planning |
| `code_completion` | Code Completion | code | Real-time code completion |
| `code_debugging` | Code Debugging | code | Debug and fix code errors |
| `code_execution` | Code Execution | code | Execute code in sandboxed environment |
| `code_generation` | Code Generation | code | Generate code in any programming language |
| `code_review` | Code Review | code | Review code for bugs, security, best practices |
| `documentation_generation` | Documentation Generation | code | Generate code documentation |
| `test_generation` | Test Generation | code | Generate unit tests for code |
| `ascension_activism` | Ascension Activism | community | Civic action, advocacy, and community organizing |
| `ascension_volunteering` | Ascension Volunteering | community | Service, volunteering, and community contribution matching |
| `ascension_air_fryer` | Ascension Air Fryer | cooking | Air fryer recipes, timing, and conversions |
| `ascension_bbq` | Ascension BBQ | cooking | BBQ styles, rubs, and techniques |
| `ascension_bread_making` | Ascension Bread Making | cooking | Bread formulas, kneading, and baking |
| `ascension_dehydrator` | Ascension Dehydrator | cooking | Dehydrator recipes and storage |
| `ascension_grilling` | Ascension Grilling | cooking | Grilling techniques, heat, and timing |
| `ascension_pizza` | Ascension Pizza | cooking | Pizza dough, sauce, and oven setup |
| `ascension_pressure_cooker` | Ascension Pressure Cooker | cooking | Pressure cooker safety and recipes |
| `ascension_slow_cooker` | Ascension Slow Cooker | cooking | Slow cooker recipes and timing |
| `ascension_smoking` | Ascension Smoking | cooking | Smoking meats, woods, and temperatures |
| `ascension_sourdough` | Ascension Sourdough | cooking | Sourdough starter, fermentation, and baking |
| `ascension_sous_vide` | Ascension Sous Vide | cooking | Sous vide temperatures, times, and searing |
| `ascension_3d_printing` | Ascension 3D Printing | creation | 3D printing, slicing, and materials |
| `ascension_arduino` | Ascension Arduino | creation | Arduino projects, sensors, and code |
| `ascension_art` | Ascension Art | creation | Art techniques, critiques, and creative direction |
| `ascension_branding` | Ascension Branding | creation | Brand identity, voice, and assets |
| `ascension_cnc` | Ascension CNC | creation | CNC machining, tooling, and safety |
| `ascension_color_grading` | Ascension Color Grading | creation | Color grading, LUTs, and look development |
| `ascension_craft` | Ascension Craft | creation | Crafts, DIY, and maker project guidance |
| `ascension_creative` | Ascension Creative | creation | Writing, music, art, and content generation planning |
| `ascension_dance` | Ascension Dance | creation | Dance styles, choreography, and practice |
| `ascension_design` | Ascension Design | creation | Graphic, UX, and visual design guidance |
| `ascension_drones` | Ascension Drones | creation | Drones, flying, regulations, and repairs |
| `ascension_electronics` | Ascension Electronics | creation | Electronics basics, circuits, and components |
| `ascension_fanfiction` | Ascension Fanfiction | creation | Fanfiction writing, tropes, and platforms |
| `ascension_filmmaking` | Ascension Filmmaking | creation | Film, video, and content production guidance |
| `ascension_ham_radio` | Ascension Ham Radio | creation | Ham radio, licensing, and operation |
| `ascension_instagram` | Ascension Instagram | creation | Instagram content, reels, and growth |
| `ascension_laser_cutting` | Ascension Laser Cutting | creation | Laser cutting, engraving, and design |
| `ascension_lyrics` | Ascension Lyrics | creation | Lyric writing, rhyme, and song structure |
| `ascension_mastering` | Ascension Mastering | creation | Audio mastering, loudness, and delivery |
| `ascension_metalworking` | Ascension Metalworking | creation | Metalworking tools, forging, and finishing |
| `ascension_mixing` | Ascension Mixing | creation | Audio mixing, levels, and balance |
| `ascension_music` | Ascension Music | creation | Music theory, composition, practice, and listening guidance |
| `ascension_obs` | Ascension OBS | creation | OBS Studio setup, scenes, and streaming |
| `ascension_photography` | Ascension Photography | creation | Photography technique, composition, and editing guidance |
| `ascension_photography_gear` | Ascension Photography Gear | creation | Cameras, lenses, and photography equipment |
| `ascension_podcast` | Ascension Podcast | creation | Podcast planning, production, and distribution guidance |
| `ascension_podcast_production` | Ascension Podcast Production | creation | Podcast production, editing, and publishing |
| `ascension_poetry` | Ascension Poetry | creation | Poetry forms, technique, and writing |
| `ascension_raspberry_pi` | Ascension Raspberry Pi | creation | Raspberry Pi projects, OS, and hardware |
| `ascension_robotics` | Ascension Robotics | creation | Robotics kits, programming, and projects |
| `ascension_soldering` | Ascension Soldering | creation | Soldering, desoldering, and circuit repair |
| `ascension_sound_design` | Ascension Sound Design | creation | Sound design, Foley, and audio libraries |
| `ascension_storytelling` | Ascension Storytelling | creation | Story structure, narrative, and oral telling |
| `ascension_streaming` | Ascension Streaming | creation | Live streaming setup, platforms, and growth |
| `ascension_thumbnail` | Ascension Thumbnail | creation | Thumbnail design, text, and contrast |
| `ascension_tiktok` | Ascension TikTok | creation | TikTok content, trends, and strategy |
| `ascension_twitter` | Ascension Twitter | creation | Twitter/X content, threads, and engagement |
| `ascension_video_editing` | Ascension Video Editing | creation | Video editing, software, and workflow |
| `ascension_voiceover` | Ascension Voiceover | creation | Voiceover recording, performance, and equipment |
| `ascension_welding` | Ascension Welding | creation | Welding processes, safety, and certification |
| `ascension_woodworking` | Ascension Woodworking | creation | Woodworking projects, tools, and joinery |
| `ascension_writing` | Ascension Writing | creation | Writing craft, editing, voice, and storytelling |
| `ascension_youtube` | Ascension YouTube | creation | YouTube content, SEO, and channel growth |
| `ascension_youtube_seo` | Ascension YouTube SEO | creation | YouTube SEO, titles, and thumbnails |
| `file_analysis` | File Analysis | data | Analyze files (PDF, DOCX, images, etc.) |
| `ascension_legal` | Ascension Legal Assistant | documents | Document review, contract analysis, and legal guidance flags |
| `ascension_college` | Ascension College | education | College search, applications, and planning |
| `ascension_exam` | Ascension Exam | education | Exam preparation, strategy, and practice |
| `ascension_homework` | Ascension Homework | education | Homework help, explanation, and study guidance |
| `ascension_memorization` | Ascension Memorization | education | Memory techniques and spaced repetition |
| `ascension_presentation` | Ascension Presentation | education | Presentations, slides, and public speaking |
| `ascension_scholarship` | Ascension Scholarship | education | Scholarship search and application support |
| `ascension_school` | Ascension School | education | School selection, applications, and planning |
| `ascension_studyskills` | Ascension Study Skills | education | Study habits, note-taking, and retention |
| `ascension_teaching` | Ascension Teaching | education | Teaching methods, lesson planning, and assessment |
| `ascension_tutor` | Ascension Tutor | education | One-on-one tutoring across subjects |
| `ascension_api` | Ascension API | engineering | API design, versioning, and documentation |
| `ascension_blockchain` | Ascension Blockchain | engineering | Blockchain concepts, smart contracts, and crypto basics |
| `ascension_cicd` | Ascension CI/CD | engineering | Continuous integration and delivery guidance |
| `ascension_cloud` | Ascension Cloud | engineering | Cloud architecture, services, and cost guidance |
| `ascension_databases` | Ascension Databases | engineering | Database design, queries, and optimization |
| `ascension_devops` | Ascension DevOps | engineering | DevOps practices, pipelines, and infrastructure |
| `ascension_microservices` | Ascension Microservices | engineering | Microservices architecture and tradeoffs |
| `ascension_mining` | Ascension Mining | engineering | Crypto mining hardware and profitability |
| `ascension_monitoring` | Ascension Monitoring | engineering | Observability, logging, and alerting |
| `ascension_nodes` | Ascension Nodes | engineering | Blockchain nodes, setup, and maintenance |
| `ascension_security_tech` | Ascension Security Tech | engineering | Application and infrastructure security guidance |
| `ascension_testing` | Ascension Testing | engineering | Test strategy, automation, and quality assurance |
| `ascension_astrology` | Ascension Astrology | entertainment | Astrology chart basics and sign compatibility |
| `ascension_betting` | Ascension Betting | entertainment | Sports betting, odds, and risk management |
| `ascension_blackjack` | Ascension Blackjack | entertainment | Blackjack strategy and odds |
| `ascension_boardgames` | Ascension Board Games | entertainment | Board game rules, strategy, and recommendations |
| `ascension_books` | Ascension Books | entertainment | Book recommendations, analysis, and reading planning |
| `ascension_casino` | Ascension Casino | entertainment | Casino game odds, strategy, and risk awareness |
| `ascension_chess` | Ascension Chess | entertainment | Chess openings, tactics, and strategy |
| `ascension_comedy` | Ascension Comedy | entertainment | Comedy writing, timing, and performance |
| `ascension_comics` | Ascension Comics | entertainment | Comic books, grading, and collecting |
| `ascension_concerts` | Ascension Concerts | entertainment | Concert planning, tickets, and etiquette |
| `ascension_cosplay` | Ascension Cosplay | entertainment | Cosplay design, construction, and events |
| `ascension_festivals` | Ascension Festivals | entertainment | Festival planning, packing, and safety |
| `ascension_games` | Ascension Games | entertainment | Game recommendations, strategy, and design discussion |
| `ascension_horoscope` | Ascension Horoscope | entertainment | Horoscope, astrology, and personal sign guidance |
| `ascension_jokes` | Ascension Jokes | entertainment | Joke writing, setups, and punchlines |
| `ascension_karaoke` | Ascension Karaoke | entertainment | Karaoke song choice, setup, and fun |
| `ascension_lottery` | Ascension Lottery | entertainment | Lottery odds and expectation guidance |
| `ascension_magic` | Ascension Magic | entertainment | Magic tricks, sleight of hand, and performance |
| `ascension_movies` | Ascension Movies | entertainment | Film and TV recommendations, analysis, and watch planning |
| `ascension_poker` | Ascension Poker | entertainment | Poker strategy, odds, and bankroll |
| `ascension_puzzles` | Ascension Puzzles | entertainment | Puzzles, logic, and problem-solving games |
| `ascension_rc` | Ascension RC | entertainment | RC cars, planes, boats, and maintenance |
| `ascension_riddles` | Ascension Riddles | entertainment | Riddles, brain teasers, and lateral thinking |
| `ascension_roleplay` | Ascension Roleplay | entertainment | Roleplay genres, character creation, and safety |
| `ascension_sports` | Ascension Sports | entertainment | Sports analysis, training, and fan engagement |
| `ascension_sports_betting` | Ascension Sports Betting | entertainment | Sports betting strategy and risk management |
| `ascension_standup` | Ascension Standup | entertainment | Stand-up comedy writing and performance |
| `ascension_tarot` | Ascension Tarot | entertainment | Tarot card meanings and reflective readings |
| `ascension_trading_cards` | Ascension Trading Cards | entertainment | Trading cards, value, and protection |
| `ascension_trivia` | Ascension Trivia | entertainment | Trivia facts, hosting, and categories |
| `ascension_environment` | Ascension Environment | environment | Sustainability, climate, and ecological action planning |
| `ascension_weather` | Ascension Weather | environment | Weather-aware planning and safety recommendations |
| `ascension_family` | Ascension FamilyOS | family | Family enterprise, tree, and governance |
| `ascension_accounting` | Ascension Accounting | finance | Accounting principles, bookkeeping, and reports |
| `ascension_airdrop` | Ascension Airdrop | finance | Airdrop farming, safety, and taxes |
| `ascension_audit` | Ascension Audit | finance | Audit preparation, documentation, and response |
| `ascension_bookkeeping` | Ascension Bookkeeping | finance | Bookkeeping entries, ledgers, and reconciliation |
| `ascension_budgeting` | Ascension Budgeting | finance | Budget creation, tracking, and variance |
| `ascension_business_taxes` | Ascension Business Taxes | finance | Business tax planning, deductions, and filing |
| `ascension_credit` | Ascension Credit | finance | Credit cards, lines, and management |
| `ascension_credit_score` | Ascension Credit Score | finance | Credit score building and repair |
| `ascension_crypto` | Ascension Crypto | finance | Cryptocurrency basics, custody, and safety |
| `ascension_dao` | Ascension DAO | finance | DAO governance and participation |
| `ascension_daytrading` | Ascension Day Trading | finance | Day trading strategy, risk, and psychology |
| `ascension_defi` | Ascension DeFi | finance | DeFi protocols, yields, and risks |
| `ascension_debt` | Ascension Debt | finance | Debt payoff, consolidation, and strategy |
| `ascension_deductible` | Ascension Deductible | finance | Deductible strategy and tradeoffs |
| `ascension_earthquake_insurance` | Ascension Earthquake Insurance | finance | Earthquake coverage and risk |
| `ascension_expenses` | Ascension Expenses | finance | Expense tracking, reimbursement, and policies |
| `ascension_fsa` | Ascension FSA | finance | Flexible Spending Accounts and planning |
| `ascension_finance` | Ascension Financial Intelligence | finance | Financial analysis, planning, and opportunity finding |
| `ascension_flood_insurance` | Ascension Flood Insurance | finance | Flood insurance, zones, and claims |
| `ascension_forex` | Ascension Forex | finance | Forex basics, pairs, and risk |
| `ascension_hsa` | Ascension HSA | finance | Health Savings Accounts and strategy |
| `ascension_insurance` | Ascension Insurance | finance | Insurance review, comparison, and gap analysis |
| `ascension_insurance_review` | Ascension Insurance Review | finance | Insurance policy review and coverage gaps |
| `ascension_investing` | Ascension Investing | finance | Portfolio thinking, asset allocation, and long-term investing |
| `ascension_invoicing` | Ascension Invoicing | finance | Invoice creation, terms, and collection |
| `ascension_liability_insurance` | Ascension Liability Insurance | finance | Liability insurance types and limits |
| `ascension_loans` | Ascension Loans | finance | Loan types, terms, and applications |
| `ascension_mortgage` | Ascension Mortgage | finance | Mortgage types, rates, and refinancing |
| `ascension_nfts` | Ascension NFTs | finance | NFTs, marketplaces, and valuation |
| `ascension_payroll` | Ascension Payroll | finance | Payroll processing, taxes, and compliance |
| `ascension_pet_insurance` | Ascension Pet Insurance | finance | Pet insurance plans and claims |
| `ascension_policy_review` | Ascension Policy Review | finance | Policy terms, exclusions, and renewals |
| `ascension_premium` | Ascension Premium | finance | Premium pricing, payment, and discounts |
| `ascension_presale` | Ascension Presale | finance | Presale research, red flags, and allocation |
| `ascension_staking` | Ascension Staking | finance | Staking, yields, and validator selection |
| `ascension_swingtrading` | Ascension Swing Trading | finance | Swing trading setups and position management |
| `ascension_taxes` | Ascension Taxes | finance | Tax organization, deduction discovery, and preparer coordination |
| `ascension_trading` | Ascension Trading Intelligence | finance | Multi-market analysis, backtesting, and paper trading |
| `ascension_umbrella_insurance` | Ascension Umbrella Insurance | finance | Umbrella policy limits and use cases |
| `ascension_whitelist` | Ascension Whitelist | finance | Whitelist registration and security |
| `ascension_post_workout` | Ascension Post Workout | fitness | Post-workout nutrition and recovery |
| `ascension_pre_workout` | Ascension Pre Workout | fitness | Pre-workout nutrition, timing, and ingredients |
| `ascension_aging` | Ascension Aging | health | Healthy aging, longevity, and life-stage adaptation |
| `ascension_fitness` | Ascension Fitness | health | Workout plans, form guidance, and progress tracking |
| `ascension_health` | Ascension Health | health | Health, wellness, and symptom guidance |
| `ascension_nutrition` | Ascension Nutrition | health | Meal planning, nutrition analysis, and dietary guidance |
| `ascension_sleep` | Ascension Sleep | health | Sleep hygiene, circadian rhythm, and recovery planning |
| `emotional_intelligence` | Emotional Intelligence | health | Emotional intelligence and tracking |
| `ascension_aquaponics` | Ascension Aquaponics | home | Aquaponics systems, fish, and plants |
| `ascension_automotive` | Ascension Automotive | home | Vehicle maintenance, diagnostics, and buying guidance |
| `ascension_baking` | Ascension Baking | home | Baking recipes, technique, and troubleshooting |
| `ascension_balcony` | Ascension Balcony | home | Balcony, patio, and small outdoor space use |
| `ascension_canning` | Ascension Canning | home | Canning methods, safety, and storage |
| `ascension_cleaning` | Ascension Cleaning | home | Cleaning routines, schedules, and product guidance |
| `ascension_commute` | Ascension Commute | home | Commute planning, routes, and optimization |
| `ascension_composting` | Ascension Composting | home | Composting methods, balance, and use |
| `ascension_cooking` | Ascension Cooking | home | Meal planning, recipes, and kitchen guidance |
| `ascension_decor` | Ascension Decor | home | Decor choices, themes, and styling |
| `ascension_events` | Ascension Events | home | Event planning, coordination, and logistics |
| `ascension_fermentation` | Ascension Fermentation | home | Fermentation, pickles, and safety |
| `ascension_garden` | Ascension Garden | home | Garden planning, plant care, and growing guidance |
| `ascension_gardening` | Ascension Gardening | home | Garden planning, planting, and care |
| `ascension_grocery_list` | Ascension Grocery List | home | Grocery list creation, pantry check, and budget |
| `ascension_home` | Ascension HomeOS | home | Household and co-parenting coordination |
| `ascension_hydroponics` | Ascension Hydroponics | home | Hydroponic systems, nutrients, and crops |
| `ascension_interior_design` | Ascension Interior Design | home | Interior layout, color, and decor planning |
| `ascension_landscaping` | Ascension Landscaping | home | Landscape design, plants, and maintenance |
| `ascension_laundry` | Ascension Laundry | home | Laundry routines, stains, and care |
| `ascension_lawn_care` | Ascension Lawn Care | home | Lawn care, mowing, and fertilization |
| `ascension_lighting` | Ascension Lighting | home | Lighting design, bulbs, and ambiance |
| `ascension_mixology` | Ascension Mixology | home | Cocktail, mocktail, and beverage guidance |
| `ascension_moving` | Ascension Moving | home | Relocation planning, checklists, and logistics |
| `ascension_organizing` | Ascension Organizing | home | Organization systems and decluttering |
| `ascension_packing` | Ascension Packing | home | Packing lists and travel preparation |
| `ascension_parenting` | Ascension Parenting | home | Child development, discipline, co-parenting, and parent support |
| `ascension_pets` | Ascension Pets | home | Pet care, health, training, and nutrition guidance |
| `ascension_preserving` | Ascension Preserving | home | Food preservation, canning, and drying |
| `ascension_realestate` | Ascension Real Estate | home | Housing search, lease review, and property analysis |
| `ascension_repair` | Ascension Repair | home | DIY repairs, maintenance, and when-to-call-a-pro guidance |
| `ascension_smell` | Ascension Smell | home | Scent, air quality, and fragrance guidance |
| `ascension_sound` | Ascension Sound | home | Sound, acoustics, and noise management |
| `ascension_storage` | Ascension Storage | home | Storage solutions and space planning |
| `ascension_travel` | Ascension Travel | home | Trip planning, flight search, and itinerary preparation |
| `ascension_grief` | Ascension Grief | human_life | Loss, bereavement, transition, and emotional support |
| `ascension_human_life` | Ascension Human Life | human_life | Comprehensive guidance across identity, health, money, relationships, home, time, learning, creativity, meaning, and transitions |
| `context_memory` | Context Memory | intelligence | Context-aware memory (characters, arcs, themes) |
| `intelligence_sweep` | Intelligence Sweep | intelligence | Intelligence sweep across 10 domains |
| `proactive_intelligence` | Proactive Intelligence | intelligence | Proactive AP behavior with push notifications |
| `ascension_argumentation` | Ascension Argumentation | knowledge | Argument structure and evidence |
| `ascension_astronomy` | Ascension Astronomy | knowledge | Astronomy, stargazing, and equipment |
| `ascension_critical_thinking` | Ascension Critical Thinking | knowledge | Critical thinking and evaluation |
| `ascension_culture` | Ascension Culture | knowledge | Cultural understanding, etiquette, and context |
| `ascension_debate` | Ascension Debate | knowledge | Debate formats, prep, and rebuttal |
| `ascension_ethics` | Ascension Ethics | knowledge | Moral reasoning, dilemma navigation, and values clarification |
| `ascension_etiquette` | Ascension Etiquette | knowledge | Etiquette, manners, and social situation guidance |
| `ascension_fallacies` | Ascension Fallacies | knowledge | Logical fallacies and spotting them |
| `ascension_history` | Ascension History | knowledge | Historical context, events, and lessons |
| `ascension_language` | Ascension Language | knowledge | Language learning, translation, and conversation practice |
| `ascension_logic` | Ascension Logic | knowledge | Logic, reasoning, and fallacies |
| `ascension_math` | Ascension Math | knowledge | Math explanation, problem-solving, and tutoring |
| `ascension_persuasion` | Ascension Persuasion | knowledge | Persuasion principles and ethics |
| `ascension_philosophy` | Ascension Philosophy | knowledge | Philosophical questions, schools of thought, and ethical reasoning |
| `ascension_science` | Ascension Science | knowledge | Scientific concepts, literacy, and exploration |
| `ascension_learning` | Ascension Learning | learning | Adaptive skill paths, practice generation, and concept explanation |
| `ascension_adoption` | Ascension Adoption | legal | Adoption information, steps, and resources |
| `ascension_contracts` | Ascension Contracts | legal | Contract review preparation and plain-language explanations |
| `ascension_custody` | Ascension Custody | legal | Child custody information and co-parenting resources |
| `ascension_divorce` | Ascension Divorce | legal | Divorce information and resource guidance |
| `ascension_immigration` | Ascension Immigration | legal | Immigration path overview and document organization |
| `ascension_landlord` | Ascension Landlord | legal | Landlord responsibilities, leases, and tenant issues |
| `ascension_prenup` | Ascension Prenup | legal | Prenuptial agreement information and attorney referral |
| `ascension_tenant` | Ascension Tenant | legal | Tenant rights, leases, and rental issues |
| `ascension_trust` | Ascension Trust | legal | Trust basics and estate planning guidance |
| `ascension_will` | Ascension Will | legal | Will planning and estate introduction |
| `ascension_anniversary` | Ascension Anniversary | life_events | Anniversary celebration and gift ideas |
| `ascension_babyshower` | Ascension Baby Shower | life_events | Baby shower planning and registry guidance |
| `ascension_birthday` | Ascension Birthday | life_events | Birthday planning, themes, and gift ideas |
| `ascension_funeral` | Ascension Funeral | life_events | Funeral planning, grief, and memorial support |
| `ascension_gift` | Ascension Gift | life_events | Gift ideas, wrapping, and giving guidance |
| `ascension_graduation` | Ascension Graduation | life_events | Graduation planning, gifts, and next steps |
| `ascension_holiday` | Ascension Holiday | life_events | Holiday planning, traditions, and travel |
| `ascension_party` | Ascension Party | life_events | Party planning, guest lists, and logistics |
| `ascension_retirement` | Ascension Retirement | life_events | Retirement planning, lifestyle, and transitions |
| `ascension_wedding` | Ascension Wedding | life_events | Wedding planning, timeline, and etiquette |
| `ascension_antiques` | Ascension Antiques | lifestyle | Antique identification, value, and care |
| `ascension_auction` | Ascension Auction | lifestyle | Auction bidding, valuation, and strategy |
| `ascension_coins` | Ascension Coins | lifestyle | Coin collecting and numismatics |
| `ascension_collector` | Ascension Collector | lifestyle | Collecting strategy, valuation, and curation |
| `ascension_fashion` | Ascension Fashion | lifestyle | Style, wardrobe, and occasion-appropriate dressing |
| `ascension_shopping` | Ascension Shopping | lifestyle | Product research, comparison, and value-based buying |
| `ascension_stamps` | Ascension Stamps | lifestyle | Stamp collecting and valuation |
| `ascension_vinyl` | Ascension Vinyl | lifestyle | Vinyl records, collecting, and care |
| `ascension_batch_cooking` | Ascension Batch Cooking | nutrition | Batch cooking plans and reheating |
| `ascension_freezer_meals` | Ascension Freezer Meals | nutrition | Freezer meal recipes and storage |
| `ascension_juicing` | Ascension Juicing | nutrition | Juicing recipes, produce, and cleanup |
| `ascension_meal_planning` | Ascension Meal Planning | nutrition | Weekly meal plans, balance, and shopping |
| `ascension_meal_prep` | Ascension Meal Prep | nutrition | Meal prep, containers, and storage |
| `ascension_protein` | Ascension Protein | nutrition | Protein sources, timing, and targets |
| `ascension_smoothies` | Ascension Smoothies | nutrition | Smoothie blends, protein, and macros |
| `ascension_supplements_stack` | Ascension Supplements Stack | nutrition | Supplement stacking, timing, and safety |
| `ascension_focus` | Ascension Focus | productivity | Deep work, attention management, and distraction reduction |
| `ascension_meetings` | Ascension Meetings | productivity | Meeting transcription, summaries, and action-item extraction |
| `ascension_time` | Ascension Time | productivity | Time management, energy mapping, priorities, and anti-procrastination |
| `ascension_addiction` | Ascension Addiction | psychology | Substance and behavioral addiction support, recovery, and professional referrals |
| `ascension_communication` | Ascension Communication | psychology | Difficult conversations, feedback, listening, and conflict resolution |
| `ascension_confidence` | Ascension Confidence | psychology | Self-efficacy, confidence building, and self-doubt navigation |
| `ascension_conflict` | Ascension Conflict | psychology | Dispute resolution, de-escalation, and repair strategies |
| `ascension_habits` | Ascension Habits | psychology | Habit formation, behavior change, cue-routine-reward loops, and identity-based change |
| `ascension_mental_health` | Ascension Mental Health | psychology | Stress, anxiety, mood, therapy navigation, and emotional regulation |
| `ascension_psychology` | Ascension Psychology | psychology | Human behavior, emotion, motivation, cognition, and mental health guidance |
| `ascension_stress` | Ascension Stress | psychology | Stress recognition, regulation, recovery, and burnout prevention |
| `ascension_active_listening` | Ascension Active Listening | relationships | Active listening and reflective response |
| `ascension_assertiveness` | Ascension Assertiveness | relationships | Assertive communication and boundaries |
| `ascension_boundaries` | Ascension Boundaries | relationships | Personal boundaries and maintenance |
| `ascension_charisma` | Ascension Charisma | relationships | Charisma, presence, and influence |
| `ascension_conflict_resolution` | Ascension Conflict Resolution | relationships | Conflict resolution and mediation |
| `ascension_dating` | Ascension Dating | relationships | Dating strategy, safety, boundaries, and communication |
| `ascension_empathy` | Ascension Empathy | relationships | Empathy, listening, and response |
| `ascension_rapport` | Ascension Rapport | relationships | Building rapport and trust |
| `ascension_relationships` | Ascension Relationships | relationships | Communication support, follow-up prep, and relationship context |
| `ascension_social` | Ascension Social | relationships | Friendship, networking, social skills, and community |
| `ascension_news` | Ascension News | research | News curation, bias awareness, and summary synthesis |
| `ascension_research` | Ascension Research | research | Deep research with source comparison and citation preparation |
| `ascension_reviews` | Ascension Reviews | research | Product, media, and service review writing |
| `ascension_security` | Ascension Security | security | Security analysis, threat flags, and privacy guidance |
| `ascension_discord` | Ascension Discord | social | Discord servers, roles, and moderation |
| `ascension_facebook` | Ascension Facebook | social | Facebook groups, pages, and events |
| `ascension_reddit` | Ascension Reddit | social | Reddit communities, posts, and etiquette |
| `relationship_graph` | Relationship Graph | social | Relationship graph engine |
| `ascension_bahai` | Ascension Baha i | spirituality | Baha i principles and practice |
| `ascension_buddhism` | Ascension Buddhism | spirituality | Buddhist concepts, practice, and meditation |
| `ascension_christianity` | Ascension Christianity | spirituality | Christian beliefs, practice, and study |
| `ascension_confucianism` | Ascension Confucianism | spirituality | Confucian values and practice |
| `ascension_druidry` | Ascension Druidry | spirituality | Druidry, nature, and ritual |
| `ascension_hinduism` | Ascension Hinduism | spirituality | Hindu philosophy, texts, and practice |
| `ascension_islam` | Ascension Islam | spirituality | Islamic beliefs, practice, and study |
| `ascension_jainism` | Ascension Jainism | spirituality | Jain beliefs and practice |
| `ascension_judaism` | Ascension Judaism | spirituality | Jewish beliefs, practice, and study |
| `ascension_meditation` | Ascension Meditation | spirituality | Guided meditation, body scans, and contemplative practices |
| `ascension_mindfulness` | Ascension Mindfulness | spirituality | Presence, meditation, breathing, and attention training |
| `ascension_native_spirituality` | Ascension Native Spirituality | spirituality | Indigenous spiritual practices and respect |
| `ascension_paganism` | Ascension Paganism | spirituality | Pagan paths, seasons, and practice |
| `ascension_shamanism` | Ascension Shamanism | spirituality | Shamanic journeying and practice |
| `ascension_shinto` | Ascension Shinto | spirituality | Shinto practice, kami, and shrines |
| `ascension_sikhism` | Ascension Sikhism | spirituality | Sikh beliefs, practice, and study |
| `ascension_spirituality` | Ascension Spirituality | spirituality | Faith, meaning, meditation, ritual, nature, legacy, and existential exploration |
| `ascension_taoism` | Ascension Taoism | spirituality | Taoist philosophy and practice |
| `ascension_wicca` | Ascension Wicca | spirituality | Wiccan practice, sabbats, and ethics |
| `ascension_baseball` | Ascension Baseball | sports | Baseball rules, strategy, and analysis |
| `ascension_basketball` | Ascension Basketball | sports | Basketball strategy, training, and analysis |
| `ascension_cricket` | Ascension Cricket | sports | Cricket rules, strategy, and fan questions |
| `ascension_esports` | Ascension Esports | sports | Esports games, teams, and strategy |
| `ascension_fantasy` | Ascension Fantasy | sports | Fantasy sports draft, lineup, and strategy |
| `ascension_football` | Ascension Football | sports | Football strategy, training, and analysis |
| `ascension_golf` | Ascension Golf | sports | Golf swing, course strategy, and equipment |
| `ascension_hockey` | Ascension Hockey | sports | Hockey rules, strategy, and training |
| `ascension_soccer` | Ascension Soccer | sports | Soccer tactics, training, and fan questions |
| `ascension_tennis` | Ascension Tennis | sports | Tennis technique, training, and matches |
| `ascension_sprout` | Ascension Sprout | sprout | Child development and learning paths |
| `ascension_bag` | Ascension Bag | style | Bag and luggage selection and care |
| `ascension_beard` | Ascension Beard | style | Beard styles, growth, and grooming |
| `ascension_haircut` | Ascension Haircut | style | Haircut styles, face shape, and maintenance |
| `ascension_jewelry` | Ascension Jewelry | style | Jewelry selection, care, and occasion matching |
| `ascension_makeup` | Ascension Makeup | style | Makeup techniques, products, and looks |
| `ascension_perfume` | Ascension Perfume | style | Fragrance, perfume, and scent guidance |
| `ascension_piercing` | Ascension Piercing | style | Piercing types, care, and safety |
| `ascension_shoes` | Ascension Shoes | style | Shoe selection, fit, and care |
| `ascension_sunglasses` | Ascension Sunglasses | style | Sunglasses, UV protection, and style |
| `ascension_tattoo` | Ascension Tattoo | style | Tattoo ideas, styles, and aftercare |
| `ascension_wallet` | Ascension Wallet | style | Wallet selection and organization |
| `ascension_watch` | Ascension Watch | style | Watch selection, care, and collection guidance |
| `ascension_chat` | Ascension Native Chat | text | General chat powered by native Ascension AI core |
| `chat_claude` | Chat Claude | text | Advanced AI chat with Claude 3.5 |
| `chat_gpt4` | Chat GPT-4 | text | Advanced AI chat with GPT-4 |
| `chat_gemini` | Chat Gemini | text | Advanced AI chat with Gemini Pro |
| `writing_document` | Document Writing | text | Write documents, reports, articles |
| `writing_email` | Email Writing | text | Write professional emails |
| `writing_marketing` | Marketing Copy | text | Generate marketing copy in brand voice |
| `writing_script` | Script Writing | text | Write video scripts, screenplays |
| `translation` | Translation | text | Translate text between 100+ languages |
| `ascension_flight` | Ascension Flight | travel | Flight booking, airports, and travel strategy |
| `ascension_public_transit` | Ascension Public Transit | travel | Public transit navigation, schedules, and tips |
| `ascension_rideshare` | Ascension Rideshare | travel | Rideshare, taxi, and driver guidance |
| `ascension_travel_insurance` | Ascension Travel Insurance | travel | Travel insurance coverage and claims |
| `video_editing` | Video Editing | video | Edit and manipulate videos |
| `video_generation_luma` | Video Generation (Luma Dream Machine) | video | Generate videos with Luma Dream Machine |
| `video_generation_pika` | Video Generation (Pika Labs) | video | Generate videos with Pika Labs |
| `video_generation_runway` | Video Generation (Runway) | video | Generate videos with Runway ML |
| `video_generation_stable` | Video Generation (Stable Video) | video | Generate videos with Stable Video Diffusion |
| `ascension_vision` | Ascension Vision | vision | Camera and environmental understanding |
| `design_generation` | Design Generation | vision | Generate designs, layouts, graphics |
| `image_editing` | Image Editing | vision | Edit and manipulate images |
| `image_generation_adobe` | Image Generation (Adobe Firefly) | vision | Generate images with Adobe Firefly |
| `image_generation_dalle` | Image Generation (DALL-E 3) | vision | Generate images with DALL-E 3 |
| `image_generation_midjourney` | Image Generation (Midjourney) | vision | Generate photorealistic images with Midjourney |
| `image_generation_stable` | Image Generation (Stable Diffusion) | vision | Generate images with Stable Diffusion |
| `ascension_voice` | Ascension Voice | voice | Voice commands, transcription, and speech-driven control |
| `web_browsing` | Web Browsing | web | Browse the web autonomously |
| `web_search` | Web Search | web | Search the web with citations |
| `ascension_affirmations` | Ascension Affirmations | wellness | Affirmations, wording, and practice |
| `ascension_allergies` | Ascension Allergies | wellness | Allergy awareness, triggers, and management |
| `ascension_archery` | Ascension Archery | wellness | Archery technique, gear, and practice |
| `ascension_boxing` | Ascension Boxing | wellness | Boxing technique, training, and conditioning |
| `ascension_breathing` | Ascension Breathing | wellness | Breathing exercises and techniques |
| `ascension_camping` | Ascension Camping | wellness | Camping gear, sites, and outdoor skills |
| `ascension_childbirth` | Ascension Childbirth | wellness | Childbirth preparation and birth plan support |
| `ascension_chronic` | Ascension Chronic | wellness | Chronic condition support and self-management guidance |
| `ascension_circadian` | Ascension Circadian | wellness | Circadian rhythm, light, and schedule |
| `ascension_climbing` | Ascension Climbing | wellness | Climbing technique, training, and safety |
| `ascension_cold_exposure` | Ascension Cold Exposure | wellness | Cold exposure, showers, and safety |
| `ascension_confidence_building` | Ascension Confidence Building | wellness | Confidence building and self-efficacy |
| `ascension_cycling` | Ascension Cycling | wellness | Cycling routes, training, and equipment |
| `ascension_disability` | Ascension Disability | wellness | Disability support, accommodations, and resources |
| `ascension_ergonomics` | Ascension Ergonomics | wellness | Desk, posture, and workspace ergonomics |
| `ascension_fencing` | Ascension Fencing | wellness | Fencing styles, gear, and training |
| `ascension_firstaid` | Ascension First Aid | wellness | First aid guidance and when to seek care |
| `ascension_fishing` | Ascension Fishing | wellness | Fishing techniques, gear, and locations |
| `ascension_gratitude` | Ascension Gratitude | wellness | Gratitude practice and reflection |
| `ascension_growth_mindset` | Ascension Growth Mindset | wellness | Growth mindset and learning attitude |
| `ascension_gymnastics` | Ascension Gymnastics | wellness | Gymnastics skills, training, and safety |
| `ascension_heat_exposure` | Ascension Heat Exposure | wellness | Sauna, hot bath, and heat safety |
| `ascension_hiking` | Ascension Hiking | wellness | Hiking preparation, trails, and safety |
| `ascension_hunting` | Ascension Hunting | wellness | Hunting safety, gear, and ethics |
| `ascension_ice_bath` | Ascension Ice Bath | wellness | Ice bath setup, duration, and safety |
| `ascension_ice_skating` | Ascension Ice Skating | wellness | Ice skating technique, gear, and rinks |
| `ascension_journaling` | Ascension Journaling | wellness | Journaling prompts, habits, and review |
| `ascension_martialarts` | Ascension Martial Arts | wellness | Martial arts style guidance, drills, and conditioning |
| `ascension_meditation_guided` | Ascension Meditation Guided | wellness | Guided meditation and relaxation |
| `ascension_mindset` | Ascension Mindset | wellness | Mindset coaching and reframes |
| `ascension_nap` | Ascension Nap | wellness | Nap length, timing, and recovery |
| `ascension_postpartum` | Ascension Postpartum | wellness | Postpartum support, recovery, and newborn adjustment |
| `ascension_pregnancy` | Ascension Pregnancy | wellness | Pregnancy planning, questions, and resource guidance |
| `ascension_recovery` | Ascension Recovery | wellness | Rest, recovery, and regeneration planning |
| `ascension_resilience` | Ascension Resilience | wellness | Resilience building and stress recovery |
| `ascension_roller_skating` | Ascension Roller Skating | wellness | Roller skating technique, gear, and spots |
| `ascension_running` | Ascension Running | wellness | Running plans, form, and training progression |
| `ascension_sauna` | Ascension Sauna | wellness | Sauna protocols, hydration, and safety |
| `ascension_shooting` | Ascension Shooting | wellness | Firearm safety, range practice, and training |
| `ascension_skateboarding` | Ascension Skateboarding | wellness | Skateboarding tricks, gear, and spots |
| `ascension_skiing` | Ascension Skiing | wellness | Skiing technique, gear, and resorts |
| `ascension_skincare` | Ascension Skincare | wellness | Skincare routines, ingredients, and concerns |
| `ascension_sleep_hygiene` | Ascension Sleep Hygiene | wellness | Sleep routines, environment, and habits |
| `ascension_snowboarding` | Ascension Snowboarding | wellness | Snowboarding technique, gear, and resorts |
| `ascension_stoicism` | Ascension Stoicism | wellness | Stoic principles and daily practice |
| `ascension_stretching` | Ascension Stretching | wellness | Stretching routines, mobility, and flexibility |
| `ascension_supplements` | Ascension Supplements | wellness | Supplement information and when to consult a clinician |
| `ascension_surfing` | Ascension Surfing | wellness | Surfing technique, waves, and board selection |
| `ascension_swimming` | Ascension Swimming | wellness | Swim technique, workouts, and training |
| `ascension_visualization` | Ascension Visualization | wellness | Visualization techniques and mental rehearsal |
| `ascension_walking` | Ascension Walking | wellness | Walking plans, routes, and fitness integration |
| `ascension_wrestling` | Ascension Wrestling | wellness | Wrestling styles, training, and technique |
| `ascension_yoga` | Ascension Yoga | wellness | Yoga poses, sequences, and practice guidance |
| `ascension_feedback` | Ascension Feedback | work | Giving and receiving feedback effectively |
| `ascension_interview` | Ascension Interview | work | Interview preparation and practice |
| `ascension_leadership` | Ascension Leadership | work | Leadership, management, and team guidance |
| `ascension_linkedin` | Ascension LinkedIn | work | LinkedIn profile, content, and networking |
| `ascension_meet` | Ascension Meet | work | Google Meet calls and settings |
| `ascension_negotiation` | Ascension Negotiation | work | Salary, contract, and negotiation strategy |
| `ascension_networking` | Ascension Networking | work | Professional networking and relationship building |
| `ascension_project` | Ascension Project | work | Project planning, milestones, and delivery tracking |
| `ascension_remote` | Ascension Remote | work | Remote work setup, routines, and collaboration |
| `ascension_resume` | Ascension Resume | work | Resume and cover letter review |
| `ascension_slack` | Ascension Slack | work | Slack workspace, channels, and bots |
| `ascension_task` | Ascension Task | work | Task breakdown, prioritization, and execution support |
| `ascension_team` | Ascension Team | work | Team dynamics, conflict, and collaboration |
| `ascension_teams` | Ascension Teams | work | Microsoft Teams meetings and collaboration |
| `ascension_webex` | Ascension Webex | work | Webex meetings and setup |
| `ascension_zoom` | Ascension Zoom | work | Zoom meetings, webinars, and setup |