<template>
  <div>
  <div class="in-file">
    <input type="file" @change="inFile($event)" multiple="multiple" accept=".xlsx, .xls" />
  </div>
    <p></p>
  <el-upload :auto-upload="false"  :on-change="elInFile"  ref="upload" class="upload-demo" accept=".xlsx, .xls">
    <el-button slot="trigger" size="mini" type="success" plain>选取文件</el-button>
    <i slot="tip" class="el-upload__tip el-icon-info">只能选取Excel</i>
  </el-upload>
</div>
</template>
<script>
import XLSX from 'xlsx'
export default {
  name: 'Upload',
  data () {
    return {
      files: null,
      fileObj: '',
      textList: 'agfdaf'
    }
  },
  methods: {
    /**
     * input-file调用此函数，默认传入$event
     * @param e {@link Object}：$event事件对象；

     */
    inFile (e) {
      this.files = (e.target || e.srcElement).files
      if (!this.files || !this.files.length) {
        return
      }
      for (let i = 0, len = this.files.length; i < len; i++) {
        this.read(this.files[i])
      }
      /* const file = e.target.files[0]
      const reader = new FileReader()
      reader.onload = e => this.$emit('load', e.target.result)
      reader.readAsText(file) */
    },
    /**
      * 文件状态改变时的钩子，添加文件、上传成功和上传失败时都会被调用。
      * @param f {@link Object}：当前上传的文件；
      * @param fs {@link Array}：当前文件列表；
      */
    elInFile (f, fs) {
      this.read(f.raw)
    },
    /**
      * 解析
      * @param f {@link File}
      */
    read (f) {
      let rd = new FileReader()
      rd.onload = e => {
        let sheets = rd.read2JS()
        for (let name in sheets) {
          console.log(name + '工作表数据：', sheets[name])
        }
        ['formulae', 'html', 'txt', 'csv', 'dif', 'slk', 'eth'].forEach(item => {
          console.info('\r\n解析为:' + item)
          let sheets = rd.read2(item)
          for (let name in sheets) {
            console.log(name + ' 工作表数据：', sheets[name])
          }
        })
      }
      rd.readAsBinaryString(f)
    }

  },
  beforeCreate () {
    FileReader.prototype.read2workbook = function () {
      let redABS = false // 是否将文件读取为二进制字符串
      let bytes = new Uint8Array(this.result) // 无符号整型数组
      var wb = null
      if (redABS) {
        let fix = fixdata(bytes)
        let b2a = btoa(fix) // js原生方法：将字符转为base64编码。对应的atob(base64)方法，将base64转字符
        wb = XLSX.read(b2a, {
          type: 'base64'
        })
      } else {
        let len = bytes.byteLength
        let binarys = new Array(len)
        for (let i = 0; i < len; i++) {
          binarys[i] = String.formCharCode(bytes[i])
        }
        let binary = binarys.join('')
        wb = XLSX.read(binary, {
          type: 'binary'
        })
      }
      return wb
    }
    FileReader.prototype.read2 = function (format = 'json') {
      let wb = this.read2workbook()
      if (!wb) {
        return null
      }
      let r = {}
      let formats = ['json', 'formulae', 'html', 'txt', 'csv', 'dif', 'slk', 'eth']
      format = formats.indexOf(format) === -1 ? 'json' : format
      wb.SheetNames.forEach(name => {
        r[name] = XLSX.utils['sheet_to' + format](wb.Sheets[name])
      })
      return r
    }
    FileReader.prototype.read2JS = function () {
      return this.read2()
    }
    FileReader.prototype.readAsBinaryString = function (f) {
      if (!this.onload) {
        this.onload = e => {
          let rs = this.read2workbook()
          console.log(rs)
        }
        this.readAsArrayBuffer(f)
      }
    }
    function fixdata (data) {
      let w = 1024 << 10
      let len = Math.floor(data.byteLength / w)
      let o = new Array(len)
      for (var i = 0; i < len; i++) {
        o[i] = String.fromCharCode.apply(null, new Uint8Array(data.slice(i * w, (i + 1) * w)))
      }
      o[i] = String.fromCharCode.apply(null, new Uint8Array(data.slice(i * w)))
      return o.join('')
    }
  }
}
</script>
<style>

</style>
<!-- https://www.w3cplus.com/vue/file-reader-component.html -->
