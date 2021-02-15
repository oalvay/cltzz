new Vue({
      el: '#result',
      data: {
        results:[]
      },
      mounted() {
        if (localStorage.getItem('results')) {
            try {
              this.results = JSON.parse(localStorage.getItem('results'));
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
      info: {
        query: '',
      },
      role:'user',
      restaurants: [],
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
      window.location.href = 'result.html';
      
    },querySearch(queryString, cb) {
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
    
  }
});