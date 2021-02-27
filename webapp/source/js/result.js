new Vue({
      el: '#result',
      data: {
        results:[],
        results_page:[],
        page_size:10,
        current_page:1,
        page_count:1,
      },
      methods: {
        handleSizeChange(val) {
          console.log(`每页 ${val} 条`);
        },
        handleCurrentChange(val) {
          cur_list =this.results.slice((val-1)*this.page_size,(val-1)*this.page_size+10);
          console.log(cur_list);
          // for (var i = 0; i < 10; i++) {
          //   this.results_page[i]=
          // }
          this.results_page=JSON.parse(JSON.stringify(cur_list));
          document.documentElement.scrollTop = 0;
        }
      },
      mounted() {
        if (localStorage.getItem('results')) {
            try {
              this.results = JSON.parse(localStorage.getItem('results'));
              this.results_page = this.results.slice(0,10)
              this.page_count = parseInt(this.results.length/this.page_size)+1
              this.$message({
                message:'Success search in '+sessionStorage.getItem('exe_time')+' seconds',
                type:'success'
              });
            } catch(e) {
              localStorage.removeItem('results');
            }
          }
        }
    });

new Vue({
  el: '#searchbar',
  data: function() {
        return {
          restaurants: [],
          state1: '',
          query: ''
        }
      },
  
  methods: {
    search(){
          var _self = this;
          axios
            .post(ip_address+'/engine/search?query='+JSON.stringify(this.query),{
  })
            .then(function (response) {
              console.log(response);
               localStorage.setItem('results',JSON.stringify(response.data.ret));
               sessionStorage.setItem('cur_query',response.data.query);
               setTimeout(() => { window.location.href = 'result.html'; }, 2000);
            })
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
  mounted() {
    if (sessionStorage.getItem('cur_query')) {
      try{
        this.query=sessionStorage.getItem('cur_query').replace(/^\"|\"$/g,'');
      }catch(e) {
              sessionStorage.removeItem('cur_query');
            }
  }
}

});