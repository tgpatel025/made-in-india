import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
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
  filteredOptions: Observable<PredictiveTermModel[]>;
  options: PredictiveTermModel[] = [];

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
    $('.search-bar-wrapper').css('border-radius', `${this.searchbarHeight / 2}px ${this.searchbarHeight / 2}px 0 0`);
    $('.search-auto-complete').css('border-radius', `0 0 ${this.searchbarHeight / 2}px ${this.searchbarHeight / 2}px`);
    $('.search-auto-complete').css('max-height', this.searchbarHeight * 5);
    $('.search-auto-complete').css('width', `${this.searchbarWidth}`);
    $('.cdk-overlay-pane').css('width', `${this.searchbarWidth}`);
    $('.cdk-overlay-pane').css('tranform', `translateX(${this.searchbarHeight + 12}px)`);
  }

  autoCompleteClosed(event) {
    $('.search-bar-wrapper').css('border-radius', `${this.searchbarHeight / 2}px`);
  }

  getInput(input: string) {
    if (this.options && this.options.length) {
      this.options.forEach(option => {
        if (option.term.match(input)) {
          this.searchString.emit(option);
        } else {
          const predictiveTerm = new PredictiveTermModel();
          predictiveTerm.term = input;
          this.searchString.emit(predictiveTerm);
        }
      });
    } else {
      const predictiveTerm = new PredictiveTermModel();
      predictiveTerm.term = input;
      this.searchString.emit(predictiveTerm);
    }
    this.options = [];
    if (input.length > 2) {
      this.apiCallService.getPredictiveTerms(input).then(response => {
        this.options = response;
      });
    }
  }

}
