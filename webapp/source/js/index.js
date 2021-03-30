
new Vue({
      el: '#searchbar',
      data: function() {
        return {
          suggestions:[],
          vocab:[],
          state1: '',
          query: '',
          suggest:'',
        }
      },
      methods: {
        currRole(selVal){
          this.role = selVal;
          sessionStorage.setItem('role', this.role);
        },
         isEmpty(obj){
              if(typeof obj == "undefined" || obj == null || obj == ""|| obj == " "){
                  return true;
              }else{
                  return false;
              }
          },

        
        search(){
          var _self = this;
          _self.$message('Searching...');
          axios
            .post(ip_address+'/engine/search?query='+JSON.stringify(this.query),{

  })
            .then(function (response) {
              console.log(response);
               localStorage.setItem('results',JSON.stringify(response.data.ret));
               sessionStorage.setItem('cur_query',response.data.query);
               sessionStorage.setItem('exe_time',response.data.exe_time);
               sessionStorage.setItem('do_you_mean',response.data.do_you_mean);
               
               setTimeout(() => { window.location.href = 'result.html'; }, 2000);
            })
            .catch(function(err){
              _self.$message({
                showClose: true,
                message: 'Failed to retreive any document! Sorry, please try another query.',
                type: 'error'
              });
            })
        },
        suggest_query(){
          // console.log('suggest',suggest)
          this.query=this.suggest;
        },
        advanced(){
          var _self = this;
          _self.$message('Searching...');
          axios
            .post(ip_address+'/engine/advanced?query='+JSON.stringify(this.query),{

  })
            .then(function (response) {
              console.log(response);
               localStorage.setItem('results',JSON.stringify(response.data.ret));
               sessionStorage.setItem('cur_query',response.data.query);
               sessionStorage.setItem('exe_time',response.data.exe_time);
               sessionStorage.setItem('do_you_mean',response.data.do_you_mean);
               
               setTimeout(() => { window.location.href = 'result.html'; }, 2000);
            })
            .catch(function(err){
              _self.$message({
                showClose: true,
                message: 'Failed to retreive any document! Sorry, please try another query.',
                type: 'error'
              });
            })
        },
        querySearch(queryString, cb) {
              if(queryString!=""){
                var words = queryString.split(' ');
                var lastwords = words.pop();
                var str = words.join(' ')

                var vocab = this.vocab;
                console.log(queryString);
                var vocabList = lastwords ? vocab.filter(this.createFilter(lastwords)) : vocab;
                vocabList = vocabList.slice(0,20)
                // 调用 callback 返回建议列表的数据
                var results = new Array()
                if(vocabList.length!=0){
                  for(var i=0;i<vocabList.length;i++){
                    var item ={'value':str+" "+ vocabList[i]}
                    results.push(item)
                  }
                  
                }
                cb(results);
              }
            },
            createStateFilter(queryString) {
              return (program) => {
                return (program.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1);
              };
            },
            createFilter(queryString) {
              return (restaurant) => {
                  return (restaurant.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
              };
            },
            loadAll() {
        },
            handleSelect(item) {
              console.log(item);
            }
        
      },
        mounted() {
          this.vocab = vocab;
          let suggest = sessionStorage.getItem('do_you_mean');
          console.log(suggest)
          if(suggest && suggest!==""){
            this.suggest=suggest.replace(/^\"|\"$/g,'');
          }
          let q = sessionStorage.getItem('cur_query');
          if(q && q!==""){
            this.query=q.replace(/^\"|\"$/g,'');
          }
          
    }
            // this.restaurants = this.loadAll();
          
    });