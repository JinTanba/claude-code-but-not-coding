---
name: video_creation
description: Use veo3 to create the optimal video for  articles.
---

## Veo 3 Few-shot Prompts Collection

### 1. **Cyberpunk City Chase**
**Scene**: Neon-lit futuristic city with flying vehicles and holographic advertisements
**Prompt**:
```
POV shot from a speeding hover bike through rain-soaked cyberpunk streets. Neon pink and blue reflections on wet asphalt, towering skyscrapers with holographic billboards flickering. Camera weaves between flying cars. Sound of rain hitting the windshield, distant sirens wailing, electric humming of engines. A voice crackles over radio: "Target approaching sector 7." Blade Runner aesthetic, cold blue tones with neon accent colors, cinematic depth of field.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "POV shot from a speeding hover bike through rain-soaked cyberpunk streets. Neon pink and blue reflections on wet asphalt, towering skyscrapers with holographic billboards flickering. Camera weaves between flying cars. Sound of rain hitting the windshield, distant sirens wailing, electric humming of engines. A voice crackles over radio: \"Target approaching sector 7.\" Blade Runner aesthetic, cold blue tones with neon accent colors, cinematic depth of field." --output_path "outputs/cyberpunk_chase.mp4"
```

### 2. **Ancient Library Discovery**
**Scene**: Dusty medieval library where magical books come to life
**Prompt**:
```
Close-up tracking shot through ancient library shelves, dust particles floating in golden sunlight streaming through stained glass windows. Books begin to glow and pages flip by themselves. An old scholar whispers: "The forbidden section awakens." Sound of rustling pages, creaking wood, mystical chimes. Camera slowly dollies forward revealing floating books. Dark academia style, warm amber lighting, shallow focus on magical elements.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Close-up tracking shot through ancient library shelves, dust particles floating in golden sunlight streaming through stained glass windows. Books begin to glow and pages flip by themselves. An old scholar whispers: \"The forbidden section awakens.\" Sound of rustling pages, creaking wood, mystical chimes. Camera slowly dollies forward revealing floating books. Dark academia style, warm amber lighting, shallow focus on magical elements." --output_path "outputs/ancient_library.mp4"
```

### 3. **Underwater Ballet**
**Scene**: Graceful jellyfish dancing in deep ocean currents
**Prompt**:
```
Wide shot of bioluminescent jellyfish performing synchronized movements in deep ocean. Their translucent bodies pulse with blue and purple light. Camera slowly rotates around the group. Muffled underwater ambience, whale songs echoing in distance, gentle water currents. Documentary style, deep blue color palette with bioluminescent highlights, smooth gimbal movements.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Wide shot of bioluminescent jellyfish performing synchronized movements in deep ocean. Their translucent bodies pulse with blue and purple light. Camera slowly rotates around the group. Muffled underwater ambience, whale songs echoing in distance, gentle water currents. Documentary style, deep blue color palette with bioluminescent highlights, smooth gimbal movements." --output_path "outputs/underwater_ballet.mp4"
```

### 4. **Street Food Sizzle**
**Scene**: Bustling Asian night market with steaming food stalls
**Prompt**:
```
Extreme close-up of street vendor's hands flipping noodles in wok, steam rising dramatically. Oil sizzles loudly, vendor shouts: "One more order coming up!" Background chatter of crowded market, clanging of utensils. Camera pulls back revealing busy night market scene. Food documentary style, warm orange lighting from stall lights, handheld camera for authentic feel.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Extreme close-up of street vendor's hands flipping noodles in wok, steam rising dramatically. Oil sizzles loudly, vendor shouts: \"One more order coming up!\" Background chatter of crowded market, clanging of utensils. Camera pulls back revealing busy night market scene. Food documentary style, warm orange lighting from stall lights, handheld camera for authentic feel." --output_path "outputs/street_food_sizzle.mp4"
```

### 5. **Arctic Aurora Dance**
**Scene**: Northern lights reflecting on frozen landscape with wolf silhouettes
**Prompt**:
```
Low angle shot of arctic wolf howling against aurora borealis sky. Green and purple lights dance across stars. Snow crunches under paws, wind whistles across ice, haunting wolf howl echoes. Camera slowly tilts up from wolf to sky. National Geographic style, cold blue-green tones contrasting with aurora colors, 24fps for cinematic motion.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Low angle shot of arctic wolf howling against aurora borealis sky. Green and purple lights dance across stars. Snow crunches under paws, wind whistles across ice, haunting wolf howl echoes. Camera slowly tilts up from wolf to sky. National Geographic style, cold blue-green tones contrasting with aurora colors, 24fps for cinematic motion." --output_path "outputs/arctic_aurora.mp4"
```

### 6. **Retro Arcade Nostalgia**
**Scene**: 1980s arcade with glowing game machines and excited teenagers
**Prompt**:
```
Steadicam shot moving through neon-lit 80s arcade. Kids exclaim: "New high score!" Machines beep and buzz, coins dropping, electronic music playing. Camera weaves between arcade cabinets, capturing excited faces illuminated by screen glow. Stranger Things aesthetic, synthwave color palette, anamorphic lens flares.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Steadicam shot moving through neon-lit 80s arcade. Kids exclaim: \"New high score!\" Machines beep and buzz, coins dropping, electronic music playing. Camera weaves between arcade cabinets, capturing excited faces illuminated by screen glow. Stranger Things aesthetic, synthwave color palette, anamorphic lens flares." --output_path "outputs/retro_arcade.mp4"
```

### 7. **Morning Coffee Ritual**
**Scene**: Cozy café with steam rising from fresh espresso
**Prompt**:
```
Macro lens close-up of espresso extraction, golden crema forming in slow motion. Steam hisses, coffee drips rhythmically, barista says softly: "Perfect extraction." Soft jazz playing, cups clinking in background. Camera pulls focus from machine to barista's satisfied smile. Lifestyle commercial style, warm browns and cream colors, shallow depth of field.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Macro lens close-up of espresso extraction, golden crema forming in slow motion. Steam hisses, coffee drips rhythmically, barista says softly: \"Perfect extraction.\" Soft jazz playing, cups clinking in background. Camera pulls focus from machine to barista's satisfied smile. Lifestyle commercial style, warm browns and cream colors, shallow depth of field." --output_path "outputs/morning_coffee.mp4"
```

### 8. **Desert Sandstorm**
**Scene**: Lone traveler walking through swirling Sahara sandstorm
**Prompt**:
```
Wide establishing shot of figure in flowing robes walking through sandstorm. Sand swirls dramatically, creating patterns in air. Wind howls intensely, fabric flapping, sand grains hitting surface. Camera slowly pushes in through sand clouds. Lawrence of Arabia cinematic style, golden hour lighting, epic scale composition.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Wide establishing shot of figure in flowing robes walking through sandstorm. Sand swirls dramatically, creating patterns in air. Wind howls intensely, fabric flapping, sand grains hitting surface. Camera slowly pushes in through sand clouds. Lawrence of Arabia cinematic style, golden hour lighting, epic scale composition." --output_path "outputs/desert_sandstorm.mp4"
```

### 9. **Tech Startup Eureka**
**Scene**: Modern office where team celebrates breakthrough
**Prompt**:
```
Handheld shot following excited programmer running through open office. "We cracked it! The algorithm works!" she shouts. Keyboards clicking, celebration cheers erupting, high-fives. Camera swirls around celebrating team. Silicon Valley documentary style, bright natural lighting, dynamic camera movement.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Handheld shot following excited programmer running through open office. \"We cracked it! The algorithm works!\" she shouts. Keyboards clicking, celebration cheers erupting, high-fives. Camera swirls around celebrating team. Silicon Valley documentary style, bright natural lighting, dynamic camera movement." --output_path "outputs/tech_startup.mp4"
```

### 10. **Enchanted Forest Portal**
**Scene**: Mystical forest where trees part to reveal glowing portal
**Prompt**:
```
Tracking shot through misty forest, ancient trees creaking and moving aside. Magical portal materializes with ethereal glow. Whispered incantation: "Through mist and shadow, the path reveals." Mystical chimes, rustling leaves, otherworldly humming. Camera slowly approaches portal. Fantasy film style like Lord of the Rings, green-blue color grading, particles floating in light beams.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Tracking shot through misty forest, ancient trees creaking and moving aside. Magical portal materializes with ethereal glow. Whispered incantation: \"Through mist and shadow, the path reveals.\" Mystical chimes, rustling leaves, otherworldly humming. Camera slowly approaches portal. Fantasy film style like Lord of the Rings, green-blue color grading, particles floating in light beams." --output_path "outputs/enchanted_forest.mp4"
```

### 11. **Japanese Garden Meditation**
**Scene**: Zen garden with koi pond and cherry blossoms
**Prompt**:
```
Slow crane shot over peaceful koi pond, cherry blossom petals falling gently. Koi fish create ripples, water trickles from bamboo fountain. Monk's voice: "In stillness, find clarity." Traditional shakuhachi flute, water sounds, gentle breeze. Terrence Malick style, natural lighting, contemplative pacing.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Slow crane shot over peaceful koi pond, cherry blossom petals falling gently. Koi fish create ripples, water trickles from bamboo fountain. Monk's voice: \"In stillness, find clarity.\" Traditional shakuhachi flute, water sounds, gentle breeze. Terrence Malick style, natural lighting, contemplative pacing." --output_path "outputs/japanese_garden.mp4"
```

### 12. **Neon Tokyo Drift**
**Scene**: Racing through Tokyo streets at night with neon reflections
**Prompt**:
```
Low angle tracking shot of sports car drifting around Shibuya corner. Tires screech, engine roars, driver yells: "Hold tight!" Neon signs blur past, rain sparkles on asphalt. J-pop from nearby store, city ambience. Fast and Furious style, high contrast neon lighting, motion blur on backgrounds.
```
**Command**:
```bash
python scripts/veo_3.py --prompt "Low angle tracking shot of sports car drifting around Shibuya corner. Tires screech, engine roars, driver yells: \"Hold tight!\" Neon signs blur past, rain sparkles on asphalt. J-pop from nearby store, city ambience. Fast and Furious style, high contrast neon lighting, motion blur on backgrounds." --output_path "outputs/neon_tokyo_drift.mp4"
```

- Please run the veo3 script in parallel for efficient processing. Video generation may take some time, so please wait until it completes.