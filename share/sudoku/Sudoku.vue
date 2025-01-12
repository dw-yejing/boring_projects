<template>
  <div class="sudoku">
    <div class="sudoku-board">
      <div v-for="(row, rowIndex) in board" :key="rowIndex" class="board-row">
        <div v-for="(cell, colIndex) in row" 
             :key="colIndex" 
             class="board-cell"
             :class="{
               'fixed': isFixed(rowIndex, colIndex),
               'selected': isSelected(rowIndex, colIndex),
               'same-number': isSameNumber(rowIndex, colIndex),
               'error': hasError(rowIndex, colIndex)
             }"
             @click="selectCell(rowIndex, colIndex)">
          {{ cell || '' }}
        </div>
      </div>
    </div>

    <div class="controls-container">
      <div class="difficulty-control">
        <select v-model="difficulty" class="difficulty-select">
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <div class="number-pad">
        <button v-for="n in 9" 
                :key="n" 
                class="number-btn"
                @click="inputNumber(n)">
          {{ n }}
        </button>
      </div>

      <div class="action-buttons">
        <button class="control-btn new-game" @click="newGame">New Game</button>
        <button class="control-btn clear" @click="inputNumber(0)">Clear</button>
        <button class="control-btn clear-all" @click="clearAll">Clear All</button>
        <button class="control-btn hint" @click="findNextHint">Hint</button>
        <button class="control-btn solution" 
                @click="toggleSolution" 
                :class="{ 'active': showingSolution }">
          {{ showingSolution ? 'Hide Solution' : 'Show Solution' }}
        </button>
      </div>
    </div>

    <!-- 加载遮罩层 -->
    <div v-if="isGenerating" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <div class="loading-text">Generating Sudoku...</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Sudoku',
  data() {
    return {
      board: Array(9).fill().map(() => Array(9).fill(0)),
      fixedCells: new Set(), // 存储初始数字的位置
      selectedCell: null,    // 当前选中的单元格
      difficulty: 'easy',    // 难度级别
      solution: null,        // 完整的解决方案
      errors: new Set(),      // 存储错误的单元格位置
      showingSolution: false, // 是否显示解答
      savedBoard: null,       // 保存显示答案前的状态
      isGenerating: false    // 新增：是否正在生成游戏
    }
  },
  mounted() {
    this.newGame()
    // 添加键盘事件监听
    window.addEventListener('keydown', this.handleKeydown)
  },
  beforeDestroy() {
    // 移除键盘事件监听
    window.removeEventListener('keydown', this.handleKeydown)
  },
  watch: {
    difficulty() {
      this.newGame()
    }
  },
  methods: {
    newGame() {
      this.errors.clear()
      this.selectedCell = null
      this.showingSolution = false
      this.savedBoard = null
      this.isGenerating = true // 开始生成时设置状态
      // 使用 setTimeout 让 UI 有机会更新
      setTimeout(() => {
        // 生成新的数独游戏
        this.generateNewGame()
        this.isGenerating = false // 生成完成后重置状态
      }, 0)
    },

    generateNewGame() {
      // 使用更可靠的生成算法
      this.board = Array(9).fill().map(() => Array(9).fill(0))
      this.fixedCells.clear()  // 移到这里，在生成新数独之前清除
      
      // 1. 先生成一个完整的有效数独
      this.fillBoard(0, 0)
      this.solution = JSON.parse(JSON.stringify(this.board))
      
      // 2. 根据难度移除数字
      const cellsToRemove = {
        easy: { min: 35, max: 40 },
        medium: { min: 45, max: 50 },
        hard: { min: 55, max: 58 }
      }[this.difficulty]
      
      this.removeNumbersWithDifficulty(cellsToRemove)
    },

    fillBoard(row, col) {
      if (col >= 9) {
        row++
        col = 0
      }
      
      if (row >= 9) {
        return true
      }
      
      // 使用随机排列的1-9数字
      const numbers = this.shuffleArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
      
      for (const num of numbers) {
        if (this.isSafeAt(this.board, row, col, num)) {
          this.board[row][col] = num
          if (this.fillBoard(row, col + 1)) {
            return true
          }
          this.board[row][col] = 0
        }
      }
      return false
    },

    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]
      }
      return array
    },

    removeNumbersWithDifficulty({ min, max }) {
      // 先把所有数字标记为固定
      for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
          if (this.board[i][j] !== 0) {
            this.fixedCells.add(`${i},${j}`)
          }
        }
      }
      
      // 创建位置列表并打乱顺序
      const positions = []
      for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
          positions.push([i, j])
        }
      }
      this.shuffleArray(positions)
      
      // 记录当前移除的数量
      let removed = 0
      const target = Math.floor(Math.random() * (max - min + 1)) + min

      for (const [row, col] of positions) {
        if (removed >= target) break;
        
        const temp = this.board[row][col]
        this.board[row][col] = 0
        this.fixedCells.delete(`${row},${col}`)
        
        // 复制当前板面用于验证
        const boardCopy = JSON.parse(JSON.stringify(this.board))
        
        // 检查是否仍然只有一个解
        if (!this.hasUniqueSolution(boardCopy)) {
          // 如果没有唯一解，恢复数字
          this.board[row][col] = temp
          this.fixedCells.add(`${row},${col}`)
        } else {
          removed++
        }
      }
    },

    hasUniqueSolution(board) {
      let solutions = 0
      
      const solve = (brd) => {
        if (solutions > 1) return // 如果已经找到多个解，提前返回
        
        let row = -1
        let col = -1
        let isEmpty = false
        
        // 找到空位置
        for (let i = 0; i < 9; i++) {
          for (let j = 0; j < 9; j++) {
            if (brd[i][j] === 0) {
              row = i
              col = j
              isEmpty = true
              break
            }
          }
          if (isEmpty) break
        }
        
        if (!isEmpty) {
          solutions++ // 找到一个解
          return
        }
        
        // 尝试填充数字
        for (let num = 1; num <= 9; num++) {
          if (this.isSafeAt(brd, row, col, num)) {
            brd[row][col] = num
            solve(brd)
            brd[row][col] = 0
          }
        }
      }
      
      solve(board)
      return solutions === 1
    },

    isSafeAt(board, row, col, num) {
      // 检查行
      for (let x = 0; x < 9; x++) {
        if (board[row][x] === num) return false
      }
      
      // 检查列
      for (let x = 0; x < 9; x++) {
        if (board[x][col] === num) return false
      }
      
      // 检查3x3方块
      const startRow = row - row % 3
      const startCol = col - col % 3
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          if (board[i + startRow][j + startCol] === num) return false
        }
      }
      
      return true
    },

    selectCell(row, col) {
      if (!this.isFixed(row, col)) {
        this.selectedCell = { row, col }
      }
    },

    inputNumber(num) {
      if (this.selectedCell) {
        const { row, col } = this.selectedCell
        this.board[row][col] = num === 0 ? 0 : num
        this.checkError(row, col)
        // 检查是否完成
        if (this.checkCompletion()) {
          setTimeout(() => {
            alert('恭喜你完成数独！')
            this.newGame()
          }, 300)
        }
      }
    },

    checkCompletion() {
      // 检查是否有空格子
      for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
          if (this.board[i][j] === 0) {
            return false
          }
        }
      }

      // 检查是否有错误
      if (this.errors.size > 0) {
        return false
      }

      // 验证每一行
      for (let row = 0; row < 9; row++) {
        const rowNums = new Set()
        for (let col = 0; col < 9; col++) {
          rowNums.add(this.board[row][col])
        }
        if (rowNums.size !== 9) return false
      }

      // 验证每一列
      for (let col = 0; col < 9; col++) {
        const colNums = new Set()
        for (let row = 0; row < 9; row++) {
          colNums.add(this.board[row][col])
        }
        if (colNums.size !== 9) return false
      }

      // 验证每个3x3方块
      for (let blockRow = 0; blockRow < 9; blockRow += 3) {
        for (let blockCol = 0; blockCol < 9; blockCol += 3) {
          const blockNums = new Set()
          for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
              blockNums.add(this.board[blockRow + i][blockCol + j])
            }
          }
          if (blockNums.size !== 9) return false
        }
      }

      return true
    },

    isFixed(row, col) {
      return this.fixedCells.has(`${row},${col}`)
    },

    isSelected(row, col) {
      return this.selectedCell && 
             this.selectedCell.row === row && 
             this.selectedCell.col === col
    },

    isSameNumber(row, col) {
      if (!this.selectedCell || this.board[row][col] === 0) return false
      const selectedNum = this.board[this.selectedCell.row][this.selectedCell.col]
      return this.board[row][col] === selectedNum
    },

    hasError(row, col) {
      return this.errors.has(`${row},${col}`)
    },

    checkError(row, col) {
      const num = this.board[row][col]
      if (num === 0) {
        this.errors.delete(`${row},${col}`)
        return
      }

      let hasError = false

      // 检查行
      for (let i = 0; i < 9; i++) {
        if (i !== col && this.board[row][i] === num) {
          hasError = true
          break
        }
      }

      // 检查列
      if (!hasError) {
        for (let i = 0; i < 9; i++) {
          if (i !== row && this.board[i][col] === num) {
            hasError = true
            break
          }
        }
      }

      // 检查3x3方块
      if (!hasError) {
        const boxRow = Math.floor(row / 3) * 3
        const boxCol = Math.floor(col / 3) * 3
        for (let i = 0; i < 3; i++) {
          for (let j = 0; j < 3; j++) {
            const currentRow = boxRow + i
            const currentCol = boxCol + j
            if (currentRow !== row && currentCol !== col && 
                this.board[currentRow][currentCol] === num) {
              hasError = true
              break
            }
          }
          if (hasError) break
        }
      }

      if (hasError) {
        this.errors.add(`${row},${col}`)
      } else {
        this.errors.delete(`${row},${col}`)
      }
    },

    handleKeydown(event) {
      // 如果按下的是数字键1-9
      if (event.key >= '1' && event.key <= '9') {
        this.inputNumber(parseInt(event.key))
        return
      }

      // 删除键或退格键清除数字
      if (event.key === 'Delete' || event.key === 'Backspace') {
        this.inputNumber(0)
        return
      }
    },

    toggleSolution() {
      this.showingSolution = !this.showingSolution;
      if (this.showingSolution) {
        // 保存当前状态
        this.savedBoard = JSON.parse(JSON.stringify(this.board));
        // 显示解答
        this.board = JSON.parse(JSON.stringify(this.solution));
      } else {
        // 恢复保存的状态
        this.board = JSON.parse(JSON.stringify(this.savedBoard));
      }
    },

    findNextHint() {
      // 1. 先尝试基础的单数法
      if (this.findSingleCandidate()) return true;
      
      // 2. 尝试隐形单数法
      if (this.findHiddenSingle()) return true;
      
      // 3. 尝试数对法
      if (this.findNakedPair()) return true;
      
      // 4. 尝试宫内数对法
      if (this.findBlockPair()) return true;
      
      // 5. 尝试X翼
      if (this.findXWing()) return true;
      
      // 6. 尝试XY链
      if (this.findXYChain()) return true;

      // 如果没有找到任何提示
      alert('没有找到可以推理出的格子！');
      return false;
    },

    // 获取某个格子的所有候选数
    getCandidates(row, col) {
      if (this.board[row][col] !== 0) return new Set();
      
      const possibilities = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9]);
      
      // 检查同行
      for (let i = 0; i < 9; i++) {
        possibilities.delete(this.board[row][i]);
      }
      
      // 检查同列
      for (let i = 0; i < 9; i++) {
        possibilities.delete(this.board[i][col]);
      }
      
      // 检查3x3方块
      const boxRow = Math.floor(row / 3) * 3;
      const boxCol = Math.floor(col / 3) * 3;
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          possibilities.delete(this.board[boxRow + i][boxCol + j]);
        }
      }
      
      return possibilities;
    },

    // 1. 基础单数法
    findSingleCandidate() {
      for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
          if (this.board[row][col] === 0) {
            const candidates = this.getCandidates(row, col);
            if (candidates.size === 1) {
              const value = Array.from(candidates)[0];
              this.selectCell(row, col);
              this.inputNumber(value);
              return true;
            }
          }
        }
      }
      return false;
    },

    // 2. 隐形单数法
    findHiddenSingle() {
      // 检查行
      for (let row = 0; row < 9; row++) {
        const candidatesMap = new Map();
        for (let col = 0; col < 9; col++) {
          if (this.board[row][col] === 0) {
            const candidates = this.getCandidates(row, col);
            candidates.forEach(num => {
              if (!candidatesMap.has(num)) candidatesMap.set(num, []);
              candidatesMap.get(num).push([row, col]);
            });
          }
        }
        // 检查是否有数字只出现在一个位置
        for (const [num, positions] of candidatesMap) {
          if (positions.length === 1) {
            const [r, c] = positions[0];
            this.selectCell(r, c);
            this.inputNumber(num);
            return true;
          }
        }
      }

      // 检查列
      for (let col = 0; col < 9; col++) {
        const candidatesMap = new Map();
        for (let row = 0; row < 9; row++) {
          if (this.board[row][col] === 0) {
            const candidates = this.getCandidates(row, col);
            candidates.forEach(num => {
              if (!candidatesMap.has(num)) candidatesMap.set(num, []);
              candidatesMap.get(num).push([row, col]);
            });
          }
        }
        for (const [num, positions] of candidatesMap) {
          if (positions.length === 1) {
            const [r, c] = positions[0];
            this.selectCell(r, c);
            this.inputNumber(num);
            return true;
          }
        }
      }

      // 检查3x3宫格
      for (let blockRow = 0; blockRow < 9; blockRow += 3) {
        for (let blockCol = 0; blockCol < 9; blockCol += 3) {
          const candidatesMap = new Map();
          for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
              const row = blockRow + i;
              const col = blockCol + j;
              if (this.board[row][col] === 0) {
                const candidates = this.getCandidates(row, col);
                candidates.forEach(num => {
                  if (!candidatesMap.has(num)) candidatesMap.set(num, []);
                  candidatesMap.get(num).push([row, col]);
                });
              }
            }
          }
          for (const [num, positions] of candidatesMap) {
            if (positions.length === 1) {
              const [r, c] = positions[0];
              this.selectCell(r, c);
              this.inputNumber(num);
              return true;
            }
          }
        }
      }
      return false;
    },

    // 3. 数对法
    findNakedPair() {
      // 检查行
      for (let row = 0; row < 9; row++) {
        const cellsWithCandidates = [];
        for (let col = 0; col < 9; col++) {
          if (this.board[row][col] === 0) {
            const candidates = this.getCandidates(row, col);
            if (candidates.size === 2) {
              cellsWithCandidates.push({
                pos: [row, col],
                candidates: Array.from(candidates)
              });
            }
          }
        }
        // 查找相同的数对
        for (let i = 0; i < cellsWithCandidates.length - 1; i++) {
          for (let j = i + 1; j < cellsWithCandidates.length; j++) {
            const pair1 = cellsWithCandidates[i];
            const pair2 = cellsWithCandidates[j];
            if (pair1.candidates.toString() === pair2.candidates.toString()) {
              // 找到数对，从其他格子中删除这两个数字
              for (let col = 0; col < 9; col++) {
                if (this.board[row][col] === 0 &&
                    col !== pair1.pos[1] && col !== pair2.pos[1]) {
                  const candidates = this.getCandidates(row, col);
                  const originalSize = candidates.size;
                  pair1.candidates.forEach(num => candidates.delete(num));
                  if (candidates.size === 1 && candidates.size < originalSize) {
                    this.selectCell(row, col);
                    this.inputNumber(Array.from(candidates)[0]);
                    return true;
                  }
                }
              }
            }
          }
        }
      }

      // 检查列
      for (let col = 0; col < 9; col++) {
        const cellsWithCandidates = [];
        for (let row = 0; row < 9; row++) {
          if (this.board[row][col] === 0) {
            const candidates = this.getCandidates(row, col);
            if (candidates.size === 2) {
              cellsWithCandidates.push({
                pos: [row, col],
                candidates: Array.from(candidates)
              });
            }
          }
        }
        // 查找相同的数对
        for (let i = 0; i < cellsWithCandidates.length - 1; i++) {
          for (let j = i + 1; j < cellsWithCandidates.length; j++) {
            const pair1 = cellsWithCandidates[i];
            const pair2 = cellsWithCandidates[j];
            if (pair1.candidates.toString() === pair2.candidates.toString()) {
              // 找到数对，从其他格子中删除这两个数字
              for (let row = 0; row < 9; row++) {
                if (this.board[row][col] === 0 &&
                    row !== pair1.pos[0] && row !== pair2.pos[0]) {
                  const candidates = this.getCandidates(row, col);
                  const originalSize = candidates.size;
                  pair1.candidates.forEach(num => candidates.delete(num));
                  if (candidates.size === 1 && candidates.size < originalSize) {
                    this.selectCell(row, col);
                    this.inputNumber(Array.from(candidates)[0]);
                    return true;
                  }
                }
              }
            }
          }
        }
      }
      return false;
    },

    // 4. 宫内数对法
    findBlockPair() {
      for (let blockRow = 0; blockRow < 9; blockRow += 3) {
        for (let blockCol = 0; blockCol < 9; blockCol += 3) {
          const cellsWithCandidates = [];
          // 收集宫内所有候选数为2的格子
          for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
              const row = blockRow + i;
              const col = blockCol + j;
              if (this.board[row][col] === 0) {
                const candidates = this.getCandidates(row, col);
                if (candidates.size === 2) {
                  cellsWithCandidates.push({
                    pos: [row, col],
                    candidates: Array.from(candidates)
                  });
                }
              }
            }
          }
          // 查找相同的数对
          for (let i = 0; i < cellsWithCandidates.length - 1; i++) {
            for (let j = i + 1; j < cellsWithCandidates.length; j++) {
              const pair1 = cellsWithCandidates[i];
              const pair2 = cellsWithCandidates[j];
              if (pair1.candidates.toString() === pair2.candidates.toString()) {
                // 从宫内其他格子中删除这两个数字
                for (let i = 0; i < 3; i++) {
                  for (let j = 0; j < 3; j++) {
                    const row = blockRow + i;
                    const col = blockCol + j;
                    if (this.board[row][col] === 0 &&
                        !(row === pair1.pos[0] && col === pair1.pos[1]) &&
                        !(row === pair2.pos[0] && col === pair2.pos[1])) {
                      const candidates = this.getCandidates(row, col);
                      const originalSize = candidates.size;
                      pair1.candidates.forEach(num => candidates.delete(num));
                      if (candidates.size === 1 && candidates.size < originalSize) {
                        this.selectCell(row, col);
                        this.inputNumber(Array.from(candidates)[0]);
                        return true;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
      return false;
    },

    // 5. X翼
    findXWing() {
      // 在行中寻找X翼
      for (let num = 1; num <= 9; num++) {
        for (let row1 = 0; row1 < 8; row1++) {
          for (let row2 = row1 + 1; row2 < 9; row2++) {
            const row1Positions = [];
            const row2Positions = [];
            
            // 收集两行中数字num可能出现的位置
            for (let col = 0; col < 9; col++) {
              if (this.board[row1][col] === 0 && 
                  this.getCandidates(row1, col).has(num)) {
                row1Positions.push(col);
              }
              if (this.board[row2][col] === 0 && 
                  this.getCandidates(row2, col).has(num)) {
                row2Positions.push(col);
              }
            }
            
            // 检查是否形成X翼
            if (row1Positions.length === 2 && 
                row2Positions.length === 2 &&
                row1Positions.toString() === row2Positions.toString()) {
              // 从这两列中删除其他行的num
              const [col1, col2] = row1Positions;
              let found = false;
              for (let row = 0; row < 9; row++) {
                if (row !== row1 && row !== row2) {
                  if (this.board[row][col1] === 0) {
                    const candidates = this.getCandidates(row, col1);
                    if (candidates.has(num) && candidates.size === 1) {
                      this.selectCell(row, col1);
                      this.inputNumber(Array.from(candidates)[0]);
                      return true;
                    }
                  }
                  if (this.board[row][col2] === 0) {
                    const candidates = this.getCandidates(row, col2);
                    if (candidates.has(num) && candidates.size === 1) {
                      this.selectCell(row, col2);
                      this.inputNumber(Array.from(candidates)[0]);
                      return true;
                    }
                  }
                }
              }
              if (found) return true;
            }
          }
        }
      }
      return false;
    },

    // 6. XY链
    findXYChain() {
      // 收集所有候选数为2的格子
      const biValueCells = [];
      for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
          if (this.board[row][col] === 0) {
            const candidates = this.getCandidates(row, col);
            if (candidates.size === 2) {
              biValueCells.push({
                pos: [row, col],
                candidates: Array.from(candidates)
              });
            }
          }
        }
      }

      // 构建XY链
      for (let start = 0; start < biValueCells.length; start++) {
        const chain = [biValueCells[start]];
        if (this.extendXYChain(chain, biValueCells)) {
          return true;
        }
      }
      return false;
    },

    // 辅助方法：扩展XY链
    extendXYChain(chain, biValueCells) {
      const lastCell = chain[chain.length - 1];
      const [lastRow, lastCol] = lastCell.pos;
      const [x, y] = lastCell.candidates;

      for (const cell of biValueCells) {
        if (chain.some(c => c.pos[0] === cell.pos[0] && c.pos[1] === cell.pos[1])) {
          continue;
        }

        const [row, col] = cell.pos;
        const candidates = cell.candidates;

        // 检查是否可以连接
        if (this.areConnected([lastRow, lastCol], [row, col]) && 
            candidates.includes(y)) {
          chain.push(cell);
          
          // 检查是否形成有效链
          if (chain.length >= 3 && this.isValidXYChain(chain)) {
            // 应用XY链的结论
            const firstCell = chain[0];
            const lastCell = chain[chain.length - 1];
            const eliminateValue = firstCell.candidates[0];

            // 检查首尾格子是否能看到相同的格子
            for (let r = 0; r < 9; r++) {
              for (let c = 0; c < 9; c++) {
                if (this.board[r][c] === 0 &&
                    this.canSeeCell([r, c], firstCell.pos) &&
                    this.canSeeCell([r, c], lastCell.pos)) {
                  const candidates = this.getCandidates(r, c);
                  if (candidates.has(eliminateValue)) {
                    candidates.delete(eliminateValue);
                    if (candidates.size === 1) {
                      this.selectCell(r, c);
                      this.inputNumber(Array.from(candidates)[0]);
                      return true;
                    }
                  }
                }
              }
            }
          }

          // 递归扩展链
          if (this.extendXYChain(chain, biValueCells)) {
            return true;
          }
          chain.pop();
        }
      }
      return false;
    },

    // 辅助方法：检查两个格子是否相连（同行、同列或同宫）
    areConnected(pos1, pos2) {
      const [row1, col1] = pos1;
      const [row2, col2] = pos2;
      return row1 === row2 || 
             col1 === col2 || 
             (Math.floor(row1/3) === Math.floor(row2/3) && 
              Math.floor(col1/3) === Math.floor(col2/3));
    },

    // 辅助方法：检查XY链是否有效
    isValidXYChain(chain) {
      const firstCell = chain[0];
      const lastCell = chain[chain.length - 1];
      return firstCell.candidates[0] === lastCell.candidates[0] ||
             firstCell.candidates[0] === lastCell.candidates[1] ||
             firstCell.candidates[1] === lastCell.candidates[0] ||
             firstCell.candidates[1] === lastCell.candidates[1];
    },

    // 辅助方法：检查一个格子是否能看到另一个格子
    canSeeCell(pos1, pos2) {
      const [row1, col1] = pos1;
      const [row2, col2] = pos2;
      return row1 === row2 || 
             col1 === col2 || 
             (Math.floor(row1/3) === Math.floor(row2/3) && 
              Math.floor(col1/3) === Math.floor(col2/3));
    },

    clearAll() {
      // 清除所有非固定格子
      for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
          if (!this.isFixed(i, j)) {
            this.board[i][j] = 0
            this.errors.delete(`${i},${j}`)
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.sudoku {
  display: flex;
  gap: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.controls-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
}

.difficulty-control {
  width: 100%;
}

.difficulty-select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.difficulty-select:hover {
  border-color: #1295DB;
}

.number-pad {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.number-btn {
  width: 45px;
  height: 45px;
  border: none;
  border-radius: 6px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 18px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.number-btn:hover {
  background: #e0e0e0;
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: auto;
}

.control-btn {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.control-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

.control-btn.new-game {
  background: #1295DB;
}

.control-btn.new-game:hover {
  background: #0f7ab3;
}

.control-btn.clear {
  background: #ff4444;
}

.control-btn.clear:hover {
  background: #ff1111;
}

.control-btn.solution {
  background: #4CAF50;
}

.control-btn.solution:hover {
  background: #45a049;
}

.control-btn.solution.active {
  background: #f57c00;
}

.control-btn.solution.active:hover {
  background: #f57c00;
}

.control-btn.clear-all {
  background: #e91e63;  /* 使用粉红色区分于单格清除 */
}

.control-btn.clear-all:hover {
  background: #d81b60;
}

.control-btn.hint {
  background: #9c27b0;  /* 使用紫色作为提示按钮的颜色 */
}

.control-btn.hint:hover {
  background: #7b1fa2;
}

/* Keep other styles unchanged */
.sudoku-board {
  display: grid;
  grid-template-rows: repeat(9, 1fr);
  gap: 0;
  background: white;
  padding: 3px;
  border: 3px solid #000000;
}

.board-row {
  display: grid;
  grid-template-columns: repeat(9, 1fr);
  gap: 0;
}

.board-cell {
  color: #2196F3;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  border: 1px solid #eee;
}

.board-cell:hover:not(.fixed) {
  background: #e8f4f9;
}

.board-cell.fixed {
  color: #000000;
  background: #f5f5f5;
  font-weight: bold;
  cursor: not-allowed;
}

.board-cell.selected {
  background: #bbdefb;
  outline: 2px dashed #2196F3;
  outline-offset: -2px;
  z-index: 1;
}

.board-cell.same-number {
  background: #e3f2fd;
}

.board-cell.error {
  color: #d32f2f;
  background: #ffebee;
}

/* 加强3x3宫格的边界 */
.board-cell:nth-child(3n):not(:last-child) {
  border-right: 2px solid #000000;
}

.board-row:nth-child(3n):not(:last-child) .board-cell {
  border-bottom: 2px solid #000000;
}

/* 修复边框重叠问题 */
.board-cell:last-child {
  border-right: none;
}

.board-row:last-child .board-cell {
  border-bottom: none;
}

/* 加载遮罩层样式 */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #1295DB;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

.loading-text {
  color: #333;
  font-size: 16px;
  font-weight: 500;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style> 