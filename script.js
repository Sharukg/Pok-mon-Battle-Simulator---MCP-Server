document.getElementById('simulate-button').addEventListener('click', async function() {
    const pokemon1Name = document.getElementById('pokemon1').value.toLowerCase().trim();
    const pokemon2Name = document.getElementById('pokemon2').value.toLowerCase().trim();

    const battleLogDiv = document.getElementById('battle-log');
    const winnerDiv = document.getElementById('winner');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    
    // Clear previous results and show loading
    battleLogDiv.textContent = '';
    winnerDiv.textContent = '';
    errorDiv.classList.add('hidden');
    loadingDiv.classList.remove('hidden');

    try {
        const response = await fetch('http://127.0.0.1:8000/v1/tools/battle_simulation_tool/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                pokemon1: pokemon1Name,
                pokemon2: pokemon2Name
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'An error occurred during the simulation.');
        }

        const data = await response.json();
        
        // Display battle log
        battleLogDiv.textContent = data.battle_log.join('\n');
        winnerDiv.textContent = `The winner is: ${data.winner}!`;
        
        // Update images based on names (using a simple mapping for this example)
        document.getElementById('p1-image').src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${getPokemonId(pokemon1Name)}.png`;
        document.getElementById('p2-image').src = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${getPokemonId(pokemon2Name)}.png`;

        // Hide loading and show winner
        loadingDiv.classList.add('hidden');
        winnerDiv.classList.remove('hidden');

    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.classList.remove('hidden');
        loadingDiv.classList.add('hidden');
    }
});

// A simple helper function to get the Pokémon ID from its name for the sprite URL
function getPokemonId(name) {
    const ids = {
        "bulbasaur": 1, "ivysaur": 2, "venusaur": 3, "charmander": 4, "charmeleon": 5, "charizard": 6,
        "squirtle": 7, "wartortle": 8, "blastoise": 9, "caterpie": 10, "metapod": 11, "butterfree": 12,
        "weedle": 13, "kakuna": 14, "beedrill": 15, "pidgey": 16, "pidgeotto": 17, "pidgeot": 18,
        "rattata": 19, "raticate": 20, "spearow": 21, "fearow": 22, "ekans": 23, "arbok": 24,
        "pikachu": 25, "raichu": 26, "sandshrew": 27, "sandslash": 28, "nidoran-f": 29, "nidorina": 30,
        "nidoqueen": 31, "nidoran-m": 32, "nidorino": 33, "nidoking": 34, "clefairy": 35, "clefable": 36,
        "vulpix": 37, "ninetales": 38, "jigglypuff": 39, "wigglytuff": 40, "zubat": 41, "golbat": 42,
        "oddish": 43, "gloom": 44, "vileplume": 45, "paras": 46, "parasect": 47, "venonat": 48,
        "venomoth": 49, "diglett": 50, "dugtrio": 51, "meowth": 52, "persian": 53, "psyduck": 54,
        "golduck": 55, "mankey": 56, "primeape": 57, "growlithe": 58, "arcanine": 59, "poliwag": 60,
        "poliwhirl": 61, "poliwrath": 62, "abra": 63, "kadabra": 64, "alakazam": 65, "machop": 66,
        "machoke": 67, "machamp": 68, "bellsprout": 69, "weepinbell": 70, "victreebel": 71, "tentacool": 72,
        "tentacruel": 73, "geodude": 74, "graveler": 75, "golem": 76, "ponyta": 77, "rapidash": 78,
        "slowpoke": 79, "slowbro": 80, "magnemite": 81, "magneton": 82, "farfetchd": 83, "doduo": 84,
        "dodrio": 85, "seel": 86, "dewgong": 87, "grimer": 88, "muk": 89, "shellder": 90, "cloyster": 91,
        "gastly": 92, "haunter": 93, "gengar": 94, "onix": 95, "drowzee": 96, "hypno": 97,
        "krabby": 98, "kingler": 99, "voltorb": 100, "electrode": 101, "exeggcute": 102, "exeggutor": 103,
        "cubone": 104, "marowak": 105, "hitmonlee": 106, "hitmonchan": 107, "lickitung": 108, "koffing": 109,
        "weezing": 110, "rhyhorn": 111, "rhydon": 112, "chansey": 113, "tangela": 114, "kangaskhan": 115,
        "horsea": 116, "seadra": 117, "goldeen": 118, "seaking": 119, "staryu": 120, "starmie": 121,
        "mr-mime": 122, "scyther": 123, "jynx": 124, "electabuzz": 125, "magmar": 126, "pinsir": 127,
        "tauros": 128, "magikarp": 129, "gyarados": 130, "lapras": 131, "ditto": 132, "eevee": 133,
        "vaporeon": 134, "jolteon": 135, "flareon": 136, "porygon": 137, "omanyte": 138, "omastar": 139,
        "kabuto": 140, "kabutops": 141, "aerodactyl": 142, "snorlax": 143, "articuno": 144, "zapdos": 145,
        "moltres": 146, "dratini": 147, "dragonair": 148, "dragonite": 149, "mewtwo": 150, "mew": 151
    };
    return ids[name] || 0; // Return 0 for not found, which will show a broken image
}