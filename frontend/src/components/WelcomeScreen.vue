<template>
  <div class="welcome-screen">
    <h2>Welcome!</h2>
    <p>Set your maze size and start your adventure.</p>
    <div class="control-group">
      <label for="maze-size">Maze Size:</label>
      <input
        type="number"
        id="maze-size"
        :value="modelValue"
        @input="$emit('update:modelValue', parseInt($event.target.value))"
        min="5"
        max="50"
      />
    </div>
    <button @click="$emit('startGame')" class="start-game-btn">
      <span v-if="loading">Loading...</span>
      <span v-else>Generate New Maze</span>
    </button>

    <div class="divider">OR</div>

    <div class="file-load-area">
      <p>Load a level from a JSON file.</p>
      <input type="file" @change="onFileChange" accept=".json" />
      <button @click="handleLoadFile" :disabled="!selectedFile || loading" class="load-file-btn">
        Load from File
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  modelValue: Number,
  loading: Boolean,
});
const emit = defineEmits(['update:modelValue', 'startGame', 'loadFile']);

const selectedFile = ref(null);

const onFileChange = (e) => {
  const files = e.target.files;
  if (files.length > 0) {
    selectedFile.value = files[0];
  }
};

const handleLoadFile = () => {
  if (selectedFile.value) {
    emit('loadFile', selectedFile.value);
  }
};
</script>

<style scoped>
.welcome-screen {
  text-align: center;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.welcome-screen h2 {
  margin-top: 0;
}

.control-group {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.start-game-btn {
  padding: 12px 25px;
  font-size: 1.1em;
  margin-top: 20px;
  background-color: #28a745;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.start-game-btn:hover {
  background-color: #218838;
}

.divider {
  margin: 20px 0;
  font-weight: bold;
  color: #666;
}

.file-load-area {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.file-load-area p {
  margin-bottom: 10px;
}

.load-file-btn {
  margin-left: 10px;
  background-color: #007bff;
}

.load-file-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
