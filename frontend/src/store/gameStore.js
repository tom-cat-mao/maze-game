import { defineStore } from 'pinia';
import ApiService from '../services/ApiService';

export const useGameStore = defineStore('game', {
  state: () => ({
    mazeData: null,
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
    puzzleSolution: null,
    puzzleTries: null,
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
      this.playerPosition = null;
      this.playerPath = [];
      this.playerScore = 0;
      this.gameWon = false;
      this.puzzleSolution = null;
      this.puzzleTries = null;
      this.bossBattleResult = null;
      this.playerSkills = null;
      this.bossHps = null;
      this.leverPuzzles = {};

      const onData = (data) => {
        if (data.maze) {
            this.mazeData = data.maze;
        }
        // Check if the final payload with boss data has arrived
        if (data.bosses && data.bosses.length > 0) {
            this.bossHps = data.bosses;
        }
        // Check for puzzle data
        if (data.lockers) {
            const puzzles = {};
            data.lockers.forEach(locker => {
                const key = `${locker.position[0]},${locker.position[1]}`;
                puzzles[key] = {
                    id: locker.id,
                    constraints: locker.tips,
                    password_hash: locker.password_hash,
                };
            });
            this.leverPuzzles = puzzles;
        }
      };

      const onComplete = () => {
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
        const response = await ApiService.solveDp(this.mazeData);
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
            this.solvePuzzle(puzzleData);
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
    async solvePuzzle(puzzleData) {
      this.isLoading = true;
      this.puzzleSolution = null; // Clear previous solution
      this.puzzleTries = null;
      try {
        const response = await ApiService.solvePuzzle(puzzleData);
        this.puzzleSolution = response.data.solution;
        this.puzzleTries = response.data.tries;
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
        // Skills are still hardcoded, but boss HPs are now dynamic
        const skills = [
            {"name": "Quick Attack", "damage": 10, "cooldown": 0},
            {"name": "Heavy Slam", "damage": 25, "cooldown": 1},
        ];
        this.playerSkills = skills; // Store skills so the UI can display them
        const response = await ApiService.solveBossBattle(this.bossHps, skills);
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
