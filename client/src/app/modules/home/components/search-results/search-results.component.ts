import { Component, OnInit, HostListener, OnDestroy } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ApiCallService } from 'src/app/shared/services/api-call.service';
import { SearchResponseModel } from 'src/app/shared/models/product-details.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})
export class SearchResultsComponent implements OnInit, OnDestroy {

  searchBarWidth: number;
  searchString: string;
  searchResult: SearchResponseModel;
  displaySpinner = true;
  spinnerSubscription: Subscription;
  constructor(private route: ActivatedRoute, private apiCallService: ApiCallService) { }

  ngOnInit(): void {
    this.searchBarWidth = window.innerWidth - 200;
    this.route.queryParams.subscribe((query) => {
      if (query) {
        this.searchString = query.q;
      }
    });
    this.spinnerSubscription = this.apiCallService.showSpinner().subscribe(res => {
      this.displaySpinner = res;
    });
    this.search(this.searchString);
  }

  @HostListener('resize')
  onResize() {
    this.searchBarWidth = window.innerWidth - 200;
  }

  search(query) {
    this.apiCallService.search(query).then(response => {
      this.searchResult = response;
    });
  }

  ngOnDestroy() {

  }

}
