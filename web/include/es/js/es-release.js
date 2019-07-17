var esApp = angular.module('es.release.report', []);



esApp.service('esReleaseService', ['$http' , function ($http) {

	return{
		fetchReleases :  function () {
	    	var releases = $http.get('/api/v1/releases').then(function successCallback(response) {
			     return response.data
			 });
	       	 return releases;
		},
		fetchReleaseVariables :  function (id) {
	    	var releaseVariables = $http.get(`/api/v1/releases/${id}/variables`).then(function successCallback(response) {
			     return response.data
			 });
	       	 return releaseVariables;
		},
	}

}]);




esApp.controller('es.ReleaseViewController', ['$scope' , '$filter', 'XlrTileHelper', 'esReleaseService',function($scope, $filter, XlrTileHelper, esReleaseService) {
	var self = this
    self.hasRecords = false
	function load(){
		self.loading = true
		esReleaseService.fetchReleases().then(function (releases){
		var releaseArray = []
                var releaseSortedArray = []
		if (releases.length > 0){
                	self.hasRecords = true
				_.forEach(releases, function(release){
					if (release.status !="TEMPLATE" && release.status !="ABORTED"){
						
						esReleaseService.fetchReleaseVariables(release.id).then(function (releaseVariables) {
							console.log(releaseVariables, 'releasevariables')
						
						
						console.log(releaseVariables, 'Reassigned variables')
						 changeTicketVar = getReleaseVariable(releaseVariables, 'Release_ID')
						if (!angular.isUndefined(changeTicketVar)){
					           release.change_request = changeTicketVar.value
						}
 
						var changeStartDateVar = getReleaseVariable(releaseVariables, 'PlannedStartDateTime')
						if (!angular.isUndefined(changeStartDateVar) && !angular.isUndefined(changeStartDateVar.value)){
							release.changeStartDate = changeStartDateVar.value
						}

						var changeEndDateVar = getReleaseVariable(releaseVariables, 'PlannedEndDateTime')
						if (!angular.isUndefined(changeEndDateVar) && !angular.isUndefined(changeEndDateVar).value){
							release.changeEndDate = changeEndDateVar.value	
						}

						
						 if (release.status=="IN_PROGRESS") {
                                                   release.status="IN PROGRESS"
                                                }
                                                else {
                                                        if (release.status=="PLANNED") {
                                                           release.startDate = release.scheduledStartDate
                                                        }
                                                }

                        if (isMasterRelease(release.tags)){                             
                            release.release_type = "MASTER"
                            release.orderCode = "00"
                        }
                        else{
                            release.release_type = "SUB"
                            release.orderCode = "01"
                        }
						release.link = "/#/releases/" + release.id.replace('Applications/','').replace("/","-")

						releaseArray.push(release);
						releaseSortedArray = $filter('orderBy')(releaseArray, ['changeStartDate','change_request','orderCode','startDate','status','title'], false);
			 			self.gridOptions = createGridOptions(releaseSortedArray);
                                		self.loading = false

						});	
				}

				});
			}
            else{
                self.hasRecords = false
                self.loading = false
            }
		});
	}

	function isMasterRelease(tags){

		var re=/MASTER/;
		for (var i=0;i<tags.length;i++){
			if (re.test(tags[i])){
				return true;
			}
		}
        return false

	}

	function getReleaseVariable(variables, varname){
	console.log(variables, varname, 'Inside getReleaseVariable')
		for (var i=0;i<variables.length;i++){
			if (variables[i].key == varname){
				return variables[i];
			}
		}

	}

 	function createGridOptions(releases) {
        var filterHeaderTemplate = "<div data-ng-include=\"'partials/releases/grid/templates/name-filter-template.html'\"></div>";
        var filterCHGHeaderTemplate = "<div data-ng-include=\"'static/@project.version@/include/es/grid/chg-filter-template.html'\"></div>";
        var filterNoHeaderTemplate = "<div data-ng-include=\"'static/@project.version@/include/es/grid/empty-filter-template.html'\"></div>";
        var columnDefs = [
                {
                    displayName: "Title",
                    field: "title",
                    cellTemplate: "static/@project.version@/include/es/grid/title-cell-template.html",
                   //filterHeaderTemplate: filterHeaderTemplate,
                    enableColumnMenu: false,
                    width: '40%'
                },
                {
                    displayName: "Change Request",
                    field: "change_request",
                    cellTemplate: "static/@project.version@/include/es/grid/chg-cell-template.html",
                    filterHeaderTemplate: filterCHGHeaderTemplate,
                    enableColumnMenu: false,
                    width: '10%'
                },
                {
                    displayName: "CHG Start Date",
                    field: "changeStartDate",
                    cellTemplate: "static/@project.version@/include/es/grid/chg-start-date-cell-template.html",
                    //filterHeaderTemplate: filterNoHeaderTemplate,
                    enableColumnMenu: false,
                    width: '10%'
                },
                {
                    displayName: "CHG Due Date",
                    field: "changeEndDate",
                    cellTemplate: "static/@project.version@/include/es/grid/chg-end-date-cell-template.html",
                    //filterHeaderTemplate: filterNoHeaderTemplate,
                    enableColumnMenu: false,
                    width: '10%'
                },
                {
                    displayName: "Start Date",
                    field: "scheduledStartDate",
                    cellTemplate: "static/@project.version@/include/es/grid/start-date-cell-template.html",
                    //filterHeaderTemplate: filterNoHeaderTemplate,
                    enableColumnMenu: false,
                    width: '10%'
                },
                {
                    displayName: "Due Date",
                    field: "dueDate",
                    cellTemplate: "static/@project.version@/include/es/grid/end-date-cell-template.html",
                    //filterHeaderTemplate: filterNoHeaderTemplate,
                    enableColumnMenu: false,
                    width: '10%'
                },
                {
                    displayName: "Status",
                    field: "status",
                    cellTemplate: "static/@project.version@/include/es/grid/status-cell-template.html",
                    //filterHeaderTemplate: filterNoHeaderTemplate,
                    enableColumnMenu: false,
                    width: '10%'
                }
            ];
        return XlrTileHelper.getGridOptions(releases, columnDefs);
    }

    function refresh(){
    	load();
    }

	load();

}])



