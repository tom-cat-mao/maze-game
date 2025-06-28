<template>
  <div>
    <h3>Puzzle Details</h3>
    
    <!-- Constraints/Clues -->
    <div class="constraints-section">
      <strong>Clues:</strong>
      <ul class="clue-list">
        <li v-for="(clue, index) in formattedConstraints" :key="index">{{ clue }}</li>
      </ul>
    </div>

    <!-- Solution -->
    <div v-if="solution" class="solution-section">
      <strong>Solution:</strong>
      <div class="puzzle-password-container">
        <span v-for="(digit, index) in solution" :key="index" class="password-digit">
          {{ digit }}
        </span>
      </div>
      <p v-if="tries !== null" class="tries-count">Solved in {{ tries }} tries.</p>
    </div>
    <div v-else class="solving-indicator">
        Solving...
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  constraints: Array,
  solution: Array,
  tries: Number,
});

const formattedConstraints = computed(() => {
  if (!props.constraints) return [];
  return props.constraints.map(c => {
    if (c[0] === -1 && c[1] === -1) {
      return 'All digits are prime numbers.';
    }
    if (c[0] === -2 && c[1] === -2) {
      return 'All digits are unique.';
    }
    if (c.length === 2) {
      const [pos, type] = c;
      return `Position ${pos} is an ${type === 0 ? 'even' : 'odd'} number.`;
    }
    if (c.length === 3) {
      const revealedDigit = c.find(d => d !== -1);
      const revealedPos = c.indexOf(revealedDigit) + 1;
      return `Position ${revealedPos} is the digit ${revealedDigit}.`;
    }
    return 'Unknown clue.';
  });
});
</script>

<style scoped>
.constraints-section {
  margin-bottom: 15px;
}

.clue-list {
  list-style-type: disc;
  padding-left: 20px;
  margin-top: 5px;
}

.solution-section {
  margin-top: 10px;
}

.solving-indicator {
    font-style: italic;
    color: #6c757d;
}

.tries-count {
  font-size: 0.9em;
  color: #6c757d;
  margin-top: 8px;
}

.puzzle-password-container {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.password-digit {
  display: inline-block;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  font-weight: bold;
  border: 1px solid #ced4da;
  background-color: #e9ecef;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
}
</style>
