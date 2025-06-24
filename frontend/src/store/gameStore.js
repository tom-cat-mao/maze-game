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
    bossBattleResult: null,
    leverPuzzles: {},
  }),
  actions: {
    async generateMaze(size) {
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
      this.bossBattleResult = null;
      this.leverPuzzles = {};

      const onData = (mazeState) => {
        this.mazeData = mazeState;
      };

      const onComplete = () => {
        if (this.mazeData && this.mazeData.length > 0) {
            const puzzleTypes = ["prime", "even", "odd"];
            for (let r = 0; r < this.mazeData.length; r++) {
                for (let c = 0; c < this.mazeData[r].length; c++) {
                    const cell = this.mazeData[r][c];
                    if (cell === 'S') {
                        this.playerPosition = { r, c };
                        this.playerPath.push([r, c]);
                    } else if (cell === 'L') {
                        this.leverPuzzles[`${r},${c}`] = {
                            length: 3,
                            unique: Math.random() > 0.5,
                            type: puzzleTypes[Math.floor(Math.random() * puzzleTypes.length)],
                        };
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
          const puzzleConstraints = this.leverPuzzles[`${newR},${newC}`];
          if (puzzleConstraints) {
            this.solvePuzzle(puzzleConstraints);
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
    async solvePuzzle(constraints) {
      this.isLoading = true;
      this.puzzleSolution = null; // Clear previous solution
      try {
        const response = await ApiService.solvePuzzle(constraints);
        this.puzzleSolution = response.data.solution;
      } catch (err) {
        this.error = 'Failed to solve puzzle.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },
    async solveBossBattle() {
      this.isLoading = true;
      try {
        const bossHp = 100;
        const skills = [
            {"name": "Quick Attack", "damage": 10, "cooldown": 0},
            {"name": "Heavy Slam", "damage": 25, "cooldown": 1},
        ];
        const response = await ApiService.solveBossBattle(bossHp, skills);
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
