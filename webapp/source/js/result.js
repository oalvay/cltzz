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
        },
        detail(id){
            var _self = this;
          axios
            .post(ip_address+'/engine/detail?id='+id,{
  })
            .then(function (response) {
              // console.log(response);
               localStorage.setItem('detail',JSON.stringify(response.data.ret));
               // sessionStorage.setItem('cur_query',response.data.query);
               setTimeout(() => { 
              window.location.href = 'detail.html?id='+id; }, 2000);
            })
        }
      },
      mounted() {
        if (localStorage.getItem('results')) {
            try {
              this.results = JSON.parse(localStorage.getItem('results'));
              this.results_page = this.results.slice(0,10)
              this.page_count = parseInt(this.results.length/this.page_size)+1
              this.$message({
                message:'Successfully found '+this.results.length+' results in '+sessionStorage.getItem('exe_time')+' seconds',
                type:'success'
              });
            } catch(e) {
              localStorage.removeItem('results');
            }
          }
        },

    });
