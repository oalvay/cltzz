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
        currRole(selVal){
          this.role = selVal;
          sessionStorage.setItem('role', this.role);
        },
        search(){
          var _self = this;
          axios
            .post('http://127.0.0.1:8080/engine/search?query='+JSON.stringify(this.query),{
  })
            .then(function (response) {
              console.log(response);
               localStorage.setItem('results',JSON.stringify(response.data.ret));
               sessionStorage.setItem('cur_query',response.data.query)
               setTimeout(() => { window.location.href = 'result.html'; }, 1000);
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
          // mounted() {
          //   // this.restaurants = this.loadAll();
          // }
    });