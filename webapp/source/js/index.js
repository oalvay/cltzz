new Vue({
      el: '#searchbar',
      data: function() {
        return {
          info: {
            query: '',
          },
          restaurants: [{ "value": "三全鲜食（北新泾店）", "address": "长宁区新渔路144号" },
          { "value": "Hot honey 首尔炸鸡（仙霞路）", "address": "上海市长宁区淞虹路661号" },
          { "value": "新旺角茶餐厅", "address": "上海市普陀区真北路988号创邑金沙谷6号楼113" },
          { "value": "泷千家(天山西路店)", "address": "天山西路438号" },
          { "value": "胖仙女纸杯蛋糕（上海凌空店）", "address": "上海市长宁区金钟路968号1幢18号楼一层商铺18-101" },
          { "value": "贡茶", "address": "上海市长宁区金钟路633号" },
          { "value": "豪大大香鸡排超级奶爸", "address": "上海市嘉定区曹安公路曹安路1685号" },
          { "value": "茶芝兰（奶茶，手抓饼）", "address": "上海市普陀区同普路1435号" },
          { "value": "十二泷町", "address": "上海市北翟路1444弄81号B幢-107" },
          { "value": "星移浓缩咖啡", "address": "上海市嘉定区新郁路817号" },
          { "value": "阿姨奶茶/豪大大", "address": "嘉定区曹安路1611号" },
          { "value": "新麦甜四季甜品炸鸡", "address": "嘉定区曹安公路2383弄55号" },
          { "value": "Monica摩托主题咖啡店", "address": "嘉定区江桥镇曹安公路2409号1F，2383弄62号1F" },
          { "value": "浮生若茶（凌空soho店）", "address": "上海长宁区金钟路968号9号楼地下一层" },
          { "value": "NONO JUICE  鲜榨果汁", "address": "上海市长宁区天山西路119号" },
          { "value": "CoCo都可(北新泾店）", "address": "上海市长宁区仙霞西路" },
          { "value": "快乐柠檬（神州智慧店）", "address": "上海市长宁区天山西路567号1层R117号店铺" }],
          state1: '',
              state2: ''
        }
      },
      methods: {
        currRole(selVal){
          this.role = selVal;
          sessionStorage.setItem('role', this.role);
        },
        search(){
          var _self = this;
          //测试用数据
          var result1 =[
          {'title':'Something Just Like This','abstract':'I\'ve been reading books of old The legends and the myths Achilles and his gold Hercules and his gifts Spider-Man\'s control And Batman with his fists And clearly I don\'t see myself upon that list But she said, where\'d you wanna go? How much you'},
          {'title':'Roxanne','abstract':'Roxanne You don\'t have to put on the red light Those days are over You don\'t have to sell your body to the night Roxanne You don\'t have to wear that dress tonight Walk the streets for money You don\'t care if it\'s wrong or if it\'s right Roxanne You don\'t have to put on the red light Roxanne You don\'t have to put on the red light Roxanne (Put on the red light)'},
          {'title':'一路向北','abstract':'後視鏡裡的世界 越來越遠的道別 你轉身向北 側臉還是很美 我用眼光去追 竟聽見你的淚 在車窗外面徘徊 是我錯失的機會 你站的方位 跟我中間隔著淚 街景一直在後退 你的崩潰在窗外零碎 我一路向北 離開有你的季節'}];
          localStorage.setItem('results',JSON.stringify(result1));
          window.location.href = 'result.html';
          // $.ajax({
          //  url: "http://host:30000/search",
          //  type: 'get',
          //  dataType: 'json',
          //  contentType:"application/json",
          //  data: { info: JSON.stringify(_self.info) },
          //  success: res => {
          //    if(res.err == false){
          //      sessionStorage.setItem('result',res.data.result);
          //      _self.$message({
          //        message: 'search success',
          //        type: 'success',
          //        center: true
          //      });
          //      setTimeout(() => { window.location.href = 'result.html'; }, 1000);
          //    } else {
          //      _self.$message({
          //        message: '用户名或密码错误',
          //        type: 'error',
          //        center: true
          //      });
          //    }
          //  },
          //  error: err =>  console.log(err)
          // });
        },
        querySearch(queryString, cb) {
              var restaurants = this.restaurants;
              var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
              // 调用 callback 返回建议列表的数据
              cb(results);
            },
            createFilter(queryString) {
              return (restaurant) => {
                  return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
              };
            },
            loadAll() {
            return [];
        },
            handleSelect(item) {
              console.log(item);
            }
        
      },
          // mounted() {
          //   // this.restaurants = this.loadAll();
          // }
    });