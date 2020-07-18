import { Component, OnInit, HostListener } from '@angular/core';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.scss']
})
export class SearchResultsComponent implements OnInit {

  searchBarWidth: number;

  constructor() { }

  ngOnInit(): void {
    this.searchBarWidth = window.innerWidth - 200;
  }

  @HostListener('resize')
  onResize() {
    this.searchBarWidth = window.innerWidth - 200;
  }

}
