<template>
  <div class="maze-grid-container">
    <div v-if="!maze" class="placeholder">Generate a maze to begin</div>
    <div v-else class="maze-grid" :style="gridStyle">
      <template v-for="(row, y) in maze" :key="y">
        <div
          v-for="(cell, x) in row"
          :key="`${y}-${x}`"
          class="maze-cell"
          :class="getCellClass(cell, x, y)"
        >
          <span>{{ getCellContent(cell) }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';

const props = defineProps({
  maze: {
    type: Array,
    default: () => null,
  },
  dpPath: {
    type: Array,
    default: () => [],
  },
  greedyPath: {
    type: Array,
    default: () => [],
  },
  playerPosition: {
    type: Object,
    default: () => null,
  },
});

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${props.maze?.[0]?.length || 10}, 30px)`,
}));

const animatedDpPath = ref([]);
const animatedGreedyPath = ref([]);
const dpIntervalId = ref(null);
const greedyIntervalId = ref(null);

const animatePath = (newPath, animatedPath, intervalIdRef) => {
  // Clear any existing animation for this path
  if (intervalIdRef.value) {
    clearInterval(intervalIdRef.value);
    intervalIdRef.value = null;
  }

  animatedPath.value = [];
  if (!newPath || newPath.length === 0) {
    return; // Exit if the new path is empty or null
  }

  let index = 0;
  intervalIdRef.value = setInterval(() => {
    if (index < newPath.length) {
      animatedPath.value.push(newPath[index]);
      index++;
    } else {
      clearInterval(intervalIdRef.value);
      intervalIdRef.value = null;
    }
  }, 50); // Adjust timing for animation speed
};

watch(() => props.dpPath, (newPath) => {
  animatePath(newPath, animatedDpPath, dpIntervalId);
}, { deep: true });

watch(() => props.greedyPath, (newPath) => {
  animatePath(newPath, animatedGreedyPath, greedyIntervalId);
}, { deep: true });


const isPath = (path, x, y) => {
  return path && path.some(p => p[0] === y && p[1] === x);
};

const getCellClass = (cell, x, y) => {
  const onDpPath = isPath(animatedDpPath.value, x, y);
  const onGreedyPath = isPath(animatedGreedyPath.value, x, y);
  const isPlayer = props.playerPosition && props.playerPosition.r === y && props.playerPosition.c === x;

  return {
    player: isPlayer,
    wall: cell === '#',
    path: cell === '.',
    start: cell === 'S',
    end: cell === 'E',
    gold: cell === 'G',
    trap: cell === 'T',
    lever: cell === 'L',
    boss: cell === 'B',
    'path-dp': onDpPath && !onGreedyPath,
    'path-greedy': onGreedyPath && !onDpPath,
    'path-common': onDpPath && onGreedyPath,
  };
};

const getCellContent = (cell) => {
  const contentMap = {
    '#': '',
    '.': '',
    'S': 'S',
    'E': 'E',
    'G': '💰',
    'T': '🔥',
    'L': '🔧',
    'B': '👹',
  };
  return contentMap[cell] || '';
};
</script>

<style scoped>
.maze-grid-container {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px solid #333;
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 8px;
  min-height: 300px;
}

.placeholder {
  color: #888;
  font-size: 1.2em;
}

.maze-grid {
  display: grid;
  border: 1px solid #ccc;
}

.maze-cell {
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2em;
  box-sizing: border-box;
  transition: background-color 0.3s ease;
}

.wall { background-color: #333; }
.path { background-color: #fff; }
.start { background-color: #4caf50; }
.end { background-color: #f44336; }
.gold { background-color: #ffeb3b; }
.trap { background-color: #ff9800; }
.lever { background-color: #03a9f4; }
.boss { background-color: #9c27b0; color: white; }

.path-dp { background-color: rgba(255, 215, 0, 0.5); } /* Gold */
.path-greedy { background-color: rgba(30, 144, 255, 0.5); } /* DodgerBlue */
.path-common { background-color: rgba(124, 252, 0, 0.6); } /* LawnGreen */

.player {
  background-color: #007bff;
  border-radius: 50%;
  box-shadow: 0 0 8px #007bff;
}
</style>
