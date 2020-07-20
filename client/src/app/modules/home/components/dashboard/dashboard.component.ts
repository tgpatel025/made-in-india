import { Component, OnInit } from '@angular/core';
import { ApiCallService } from 'src/app/shared/services/api-call.service';
import { PredictiveTermModel } from 'src/app/shared/models/predictive-term.model';
import { SearchResponseModel } from 'src/app/shared/models/product-details.model';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  searchString: PredictiveTermModel = new PredictiveTermModel();
  searchResponse: SearchResponseModel = new SearchResponseModel();
  constructor(
    private apiCallService: ApiCallService
  ) { }

  ngOnInit(): void {
  }

  getSearchText(searchText: PredictiveTermModel) {
    this.searchString = searchText;
  }

  getSearchResult() {
    this.apiCallService.search(this.searchString.term, this.searchString.genericName).then(response => {
      this.searchResponse = response;
      console.log(response);
    });
  }

}
