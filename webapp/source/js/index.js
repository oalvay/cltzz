new Vue({
      el: '#searchbar',
      data: function() {
        return {
          info:{
            query: '',
          },
          restaurants: [],
          state1: '',
          query: ''
        }
      },
      methods: {
        currRole(selVal){
          this.role = selVal;
          sessionStorage.setItem('role', this.role);
        },
        search(){
          var _self = this;
          $.ajax({
           url: "http://127.0.0.1:8000/diangezi/search",
           type: 'get',
           dataType: 'json',
           contentType:"application/json",
           data: { 'query': _self.query},
           success: res => {
             if(res.err == false){
               sessionStorage.setItem('results',res.ret);
               _self.$message({
                 message: 'search success',
                 type: 'success',
                 center: true
               });
               setTimeout(() => { window.location.href = 'result.html'; }, 1000);
             } else {
               _self.$message({
                 message: '错误',
                 type: 'error',
                 center: true
               });
             }
           },
           error: err =>  console.log(err)
          });
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