import { Component, OnInit, Input, Output, EventEmitter, HostListener } from '@angular/core';
import { FormControl } from '@angular/forms';
import { map, startWith, timestamp } from 'rxjs/operators';
import { Observable } from 'rxjs';
import { ApiCallService } from '../../../../services/api-call.service';
import { PredictiveTermModel } from '../../../../models/predictive-term.model';

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

  constructor(
    private apiCallService: ApiCallService
  ) { }

  ngOnInit() {
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
    this.search();
  }

  @HostListener('window.keydown', ['$event'])
  enterDown(event: KeyboardEvent) {
    // tslint:disable-next-line: deprecation
    if (event.keyCode === 13) {
      this.search();
    }
  }

  @HostListener('window.keyup', ['$event'])
  enterUp(event: KeyboardEvent) {
    // tslint:disable-next-line: deprecation
    if (event.keyCode === 13) {
      this.search();
    }
  }

  search() {
    this.apiCallService.search(this.myControl.value).then(response => {
      console.log(response);
    });
  }

  getInput(input: string) {
    this.searchString.emit(input);
    this.apiCallService.getPredictiveTerms(input).then(response => {
      this.options = response;
    });
  }

}
