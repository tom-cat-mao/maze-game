<template>
  <div class="game-view">
    <h1>Algorithm-Driven Maze Adventure</h1>

    <!-- Welcome Screen -->
    <WelcomeScreen 
      v-if="!game.isGameActive" 
      v-model="mazeSize"
      :loading="game.isLoading"
      @startGame="handleGenerateMaze"
    />

    <!-- Main Game Content -->
    <div v-if="game.isGameActive">
        <div class="controls">
          <div class="control-group">
            <label for="maze-size-ingame">Maze Size:</label>
            <input type="number" id="maze-size-ingame" v-model.number="mazeSize" min="5" max="50">
            <button @click="handleGenerateMaze" :disabled="game.isLoading">
              {{ game.isLoading ? 'Generating...' : 'New Game' }}
            </button>
          </div>
          <div class="control-group">
            <button @click="game.solveDp()" :disabled="!game.mazeData || game.isLoading">
              {{ game.isLoading ? 'Solving...' : 'Solve with DP' }}
            </button>
            <button @click="game.solveGreedy()" :disabled="!game.mazeData || game.isLoading">
              {{ game.isLoading ? 'Solving...' : 'Solve with Greedy' }}
            </button>
          </div>
        </div>

        <div v-if="game.error" class="error-message">{{ game.error }}</div>

        <div class="results-container">
            <MazeGrid :maze="game.mazeData" :dpPath="game.dpPath" :greedyPath="game.greedyPath" :playerPosition="game.playerPosition" />
            <div class="info-panel">
                <div class="info-section">
                    <h2>Player</h2>
                    <div class="result-item">
                        <h3>Score: <span class="value-player">{{ game.playerScore }}</span></h3>
                    </div>
                </div>

                <div class="info-section">
                    <h2>Results</h2>
                    <div class="result-item">
                        <h3>Dynamic Programming</h3>
                        <p>Path: {{ game.dpPath ? 'Found' : 'N/A' }}</p>
                        <p>Value: <span class="value-dp">{{ game.dpValue }}</span></p>
                    </div>
                    <div class="result-item">
                        <h3>Greedy Algorithm</h3>
                        <p>Path: {{ game.greedyPath ? 'Found' : 'N/A' }}</p>
                        <p>Value: <span class="value-greedy">{{ game.greedyValue }}</span></p>
                    </div>
                    <div class="result-item" v-if="game.activePuzzle">
                        <PuzzleResult 
                            :constraints="game.activePuzzle.constraints"
                            :solution="game.activePuzzle.solution" 
                            :tries="game.activePuzzle.tries" 
                        />
                    </div>
                    <div class="result-item" v-if="game.bossBattleResult">
                        <BattleReport 
                            :playerSkills="game.playerSkills"
                            :bossHps="game.bossHps"
                            :battleResult="game.bossBattleResult"
                        />
                    </div>
                </div>

                <div class="info-section">
                    <div class="legend">
                        <h3>Legend</h3>
                        <ul>
                            <li><span class="swatch wall"></span> Wall</li>
                            <li><span class="swatch start"></span> Start</li>
                            <li><span class="swatch end"></span> End</li>
                            <li><span class="swatch gold"></span> Gold (G)</li>
                            <li><span class="swatch trap"></span> Trap (T)</li>
                            <li><span class="swatch lever"></span> Puzzle Lever (L)</li>
                            <li><span class="swatch boss"></span> Boss (B)</li>
                            <li><span class="swatch path-dp"></span> DP Path</li>
                            <li><span class="swatch path-greedy"></span> Greedy Path</li>
                            <li><span class="swatch path-common"></span> Common Path</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Game Won Modal -->
    <GameWonModal 
        v-if="game.gameWon"
        :score="game.playerScore"
        @playAgain="handleGenerateMaze"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useGameStore } from '../store/gameStore';
import MazeGrid from '@/components/MazeGrid.vue';
import WelcomeScreen from '@/components/WelcomeScreen.vue';
import GameWonModal from '@/components/GameWonModal.vue';
import BattleReport from '@/components/BattleReport.vue';
import PuzzleResult from '@/components/PuzzleResult.vue';

const mazeSize = ref(15);
const game = useGameStore();

const handleGenerateMaze = () => {
  game.generateMaze(mazeSize.value);
};

const handleKeyDown = (e) => {
  const keyMap = {
    'ArrowUp': 'up',
    'ArrowDown': 'down',
    'ArrowLeft': 'left',
    'ArrowRight': 'right',
  };
  if (keyMap[e.key]) {
    e.preventDefault();
    game.movePlayer(keyMap[e.key]);
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown);
});
</script>

<style scoped>
.game-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1200px;
}

h1 {
  color: #333;
}

.controls {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.control-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

button {
  padding: 10px 15px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

input {
    padding: 8px;
    border-radius: 5px;
    border: 1px solid #ccc;
    width: 60px;
}

.error-message {
  color: red;
  margin-bottom: 20px;
}

.results-container {
    display: flex;
    gap: 30px;
    width: 100%;
    justify-content: center;
}

.info-panel {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.info-section {
    background-color: #fff;
    padding: 15px;
    border-radius: 6px;
    border: 1px solid #e9ecef;
}

.info-section h2, .battle-report h3 {
    margin-top: 0;
    border-bottom: 2px solid #007bff;
    padding-bottom: 5px;
    margin-bottom: 15px;
}

/* Battle report styles are now in BattleReport.vue */

.result-item {
    margin-bottom: 15px;
}

.result-item:last-child {
    margin-bottom: 0;
}

/* Component-specific styles are now in their respective files */

.value-dp {
    color: #b8860b; /* DarkGoldenRod */
    font-weight: bold;
}

.value-greedy {
    color: #1e90ff; /* DodgerBlue */
    font-weight: bold;
}

.value-player {
    color: #28a745; /* Green */
    font-weight: bold;
}

.game-won-message {
    color: #28a745;
    font-weight: bold;
    text-align: center;
}

.legend .swatch {
    display: inline-block;
    width: 15px;
    height: 15px;
    margin-right: 8px;
    vertical-align: middle;
    border: 1px solid #ccc;
}
.legend ul {
    list-style: none;
    padding: 0;
}
.legend li {
    margin-bottom: 5px;
}

/* Add swatch colors here so the legend can use them */
.swatch.wall { background-color: #333; }
.swatch.start { background-color: #4caf50; }
.swatch.end { background-color: #f44336; }
.swatch.gold { background-color: #ffeb3b; }
.swatch.trap { background-color: #ff9800; }
.swatch.lever { background-color: #03a9f4; }
.swatch.boss { background-color: #9c27b0; }
.swatch.path-dp { background-color: rgba(255, 215, 0, 0.5); }
.swatch.path-greedy { background-color: rgba(30, 144, 255, 0.5); }
.swatch.path-common { background-color: rgba(124, 252, 0, 0.6); }
</style>
