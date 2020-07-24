import { Component, OnInit, Input, Output, EventEmitter, HostListener } from '@angular/core';
import { FormControl } from '@angular/forms';
import { map, startWith } from 'rxjs/operators';
import { ApiCallService } from '../../../../services/api-call.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss']
})
export class SearchBarComponent implements OnInit {

  myControl = new FormControl();
  options: string[] = [];

  @Input() searchbarWidth: number;
  @Input() searchbarHeight: number;
  @Output() searchString = new EventEmitter<any>();
  @Output() callForSearch = new EventEmitter<any>();

  constructor(
    private apiCallService: ApiCallService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    this.route.queryParams.subscribe(res => {
      if (res.q) {
        this.myControl.setValue(res.q);
      }
    });
    this.myControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this.getInput(value))
      );
  }


  autoCompleteOpen(event) {
    if (this.options.length) {
      $('.search-bar-wrapper').css('border-radius', `${this.searchbarHeight / 2}px ${this.searchbarHeight / 2}px 0 0`);
      $('.search-auto-complete').css('border-radius', `0 0 ${this.searchbarHeight / 2}px ${this.searchbarHeight / 2}px`);
      $('.search-auto-complete').css('max-height', this.searchbarHeight * 5);
      $('.search-auto-complete').css('width', `${this.searchbarWidth}`);
      $('.cdk-overlay-pane').css('width', `${this.searchbarWidth}`);
      $('.cdk-overlay-pane').css('tranform', `translateX(${this.searchbarHeight + 12}px)`);
    }
  }

  autoCompleteClosed(event) {
    $('.search-bar-wrapper').css('border-radius', `${this.searchbarHeight / 2}px`);
  }

  setSelectedOption(event) {
    const parsedValue = event.option.value.replace(/<[^>]*>/g, '');
    this.myControl.setValue(parsedValue);
    this.callForSearch.emit(this.myControl.value);
    this.router.navigate(['search'], {
      queryParams: {
        q: this.myControl.value
      }
    });
  }


  onKey(event) {
    if (event.keyCode === 13) {
      this.searchString.emit(this.myControl.value);
      this.callForSearch.emit(this.myControl.value);
      this.router.navigate(['search'], {
        queryParams: {
          q: this.myControl.value
        }
      });
    }
  }

  getInput(input: string) {
    this.searchString.emit(input);
    this.apiCallService.getPredictiveTerms(input).then(response => {
      this.options = response;
    });
  }

}
