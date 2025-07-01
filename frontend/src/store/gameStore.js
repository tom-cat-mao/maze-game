import { defineStore } from 'pinia';
import ApiService from '../services/ApiService';

export const useGameStore = defineStore('game', {
  state: () => ({
    mazeData: null,
    uniquePath: null, // To store the unique path from the generator
    dpPath: null,
    dpValue: 0,
    greedyPath: null,
    greedyValue: 0,
    isLoading: false,
    error: null,
    playerPosition: null,
    playerPath: [],
    playerScore: 0,
    gameWon: false,
    activePuzzle: null, // New state for the current puzzle
    bossBattleResult: null,
    playerSkills: null,
    bossHps: null,
    leverPuzzles: {},
    isGameActive: false,
  }),
  actions: {
    async generateMaze(size) {
      this.isGameActive = true;
      this.isLoading = true;
      this.error = null;
      this.mazeData = []; // Start with an empty maze for animation
      this.dpPath = null;
      this.greedyPath = null;
      this.uniquePath = null;
      this.playerPosition = null;
      this.playerPath = [];
      this.playerScore = 0;
      this.gameWon = false;
      this.activePuzzle = null;
      this.bossBattleResult = null;
      this.playerSkills = null;
      this.bossHps = null;
      this.leverPuzzles = {};
      
      const mazeQueue = [];
      let isProcessingQueue = false;

      const processQueue = () => {
        if (mazeQueue.length === 0) {
          isProcessingQueue = false;
          return;
        }
        isProcessingQueue = true;
        const data = mazeQueue.shift();
        
        if (data.maze) {
          this.mazeData = data.maze;
        }
        if (data.bosses && data.bosses.length > 0) {
          this.bossHps = data.bosses;
        }
        if (data.lockers) {
          const puzzles = {};
          data.lockers.forEach(locker => {
            const key = `${locker.position[0]},${locker.position[1]}`;
            puzzles[key] = {
              id: locker.id,
              constraints: locker.constraints,
              password_hash: locker.password_hash,
            };
          });
          this.leverPuzzles = puzzles;
        }
        if (data.player_skills) {
          this.playerSkills = data.player_skills.map((skill, index) => ({
            name: `Skill ${index + 1}`,
            damage: skill[0],
            cooldown: skill[1],
          }));
        }
        if (data.unique_path) {
          this.uniquePath = data.unique_path;
        }
        
        setTimeout(processQueue, 100); // Process next item after 100ms
      };

      const onData = (data) => {
        mazeQueue.push(data);
        if (!isProcessingQueue) {
          processQueue();
        }
      };

      const onComplete = () => {
        const finalizer = () => {
          if (isProcessingQueue) {
            // Wait until the queue is empty
            setTimeout(finalizer, 100);
            return;
          }
          if (this.mazeData && this.mazeData.length > 0) {
              for (let r = 0; r < this.mazeData.length; r++) {
                  for (let c = 0; c < this.mazeData[r].length; c++) {
                      const cell = this.mazeData[r][c];
                      if (cell === 'S') {
                          this.playerPosition = { r, c };
                          this.playerPath.push([r, c]);
                      }
                  }
              }
          }
          this.isLoading = false;
        };
        finalizer();
      };
      
      const onError = (err) => {
        this.error = 'Failed to generate maze.';
        console.error(err);
        this.isLoading = false;
      };

      // ApiService.generateMaze is now non-blocking and uses callbacks
      ApiService.generateMaze(size, onData, onComplete, onError);
    },
    async solveDp() {
      if (!this.mazeData) return;
      this.isLoading = true;
      this.error = null;
      try {
        const payload = {
          maze: this.mazeData,
          main_path: this.uniquePath, // Pass the unique path to the API
        };
        const response = await ApiService.solveDp(payload);
        this.dpPath = response.data.path;
        this.dpValue = response.data.value;
      } catch (err) {
        this.error = 'Failed to solve with Dynamic Programming.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    async solveGreedy() {
      if (!this.mazeData) return;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await ApiService.solveGreedy(this.mazeData);
        this.greedyPath = response.data.path;
        this.greedyValue = response.data.value;
      } catch (err) {
        this.error = 'Failed to solve with Greedy Algorithm.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    movePlayer(direction) {
      if (!this.playerPosition || this.gameWon) return;

      const { r, c } = this.playerPosition;
      let newR = r, newC = c;

      if (direction === 'up') newR--;
      else if (direction === 'down') newR++;
      else if (direction === 'left') newC--;
      else if (direction === 'right') newC++;

      if (
        newR >= 0 && newR < this.mazeData.length &&
        newC >= 0 && newC < this.mazeData[0].length &&
        this.mazeData[newR][newC] !== '#'
      ) {
        this.playerPosition = { r: newR, c: newC };
        this.playerPath.push([newR, newC]);
        
        const cell = this.mazeData[newR][newC];
        if (cell === 'G') {
          this.playerScore += 10;
          this.mazeData[newR][newC] = '.'; // Consume gold
        } else if (cell === 'T') {
          this.playerScore -= 5;
          this.mazeData[newR][newC] = '.'; // Consume trap
        } else if (cell === 'L') {
          this.playerScore += 5;
          this.mazeData[newR][newC] = '.'; // Consume lever
          const puzzleData = this.leverPuzzles[`${newR},${newC}`];
          if (puzzleData && puzzleData.constraints && puzzleData.password_hash) {
            this.activePuzzle = { ...puzzleData, solution: null, tries: null };
            // Automatically solve it for now, but the puzzle is now active
            this.solvePuzzle();
          }
        } else if (cell === 'B') {
          this.playerScore += 10;
          this.mazeData[newR][newC] = '.'; // Consume boss
          this.solveBossBattle();
        } else if (cell === 'E') {
          this.playerScore += 5;
          this.gameWon = true;
        }
      }
    },
    async solvePuzzle() {
      if (!this.activePuzzle) return;

      this.isLoading = true;
      try {
        const response = await ApiService.solvePuzzle(this.activePuzzle);
        this.activePuzzle.solution = response.data.solution;
        this.activePuzzle.tries = response.data.tries;
      } catch (err) {
        this.error = 'Failed to solve puzzle.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    async solveBossBattle() {
      if (!this.bossHps || this.bossHps.length === 0) {
        this.error = "No boss data available for this battle!";
        return;
      }
      this.isLoading = true;
      try {
        if (!this.playerSkills || this.playerSkills.length === 0) {
            this.error = "Player skills not available for boss battle!";
            return;
        }
        const response = await ApiService.solveBossBattle(this.bossHps, this.playerSkills);
        this.bossBattleResult = response.data;
      } catch (err) {
        this.error = 'Failed to solve boss battle.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    }
  },
});
