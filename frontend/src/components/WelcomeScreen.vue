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
      <div class="file-input-wrapper">
        <input type="file" id="file-upload" @change="onFileChange" accept=".json" class="file-input-hidden" />
        <label for="file-upload" class="file-upload-label">Browse...</label>
        <span v-if="selectedFile" class="file-name">{{ selectedFile.name }}</span>
        <button @click="handleLoadFile" :disabled="!selectedFile || loading" class="load-file-btn">
          Load from File
        </button>
      </div>
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

.file-input-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 15px;
}

.file-input-hidden {
  display: none;
}

.file-upload-label {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.file-upload-label:hover {
  background-color: #0056b3;
}

.file-name {
  font-style: italic;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.load-file-btn {
  background-color: #007bff;
  padding: 10px 15px;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.load-file-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
