import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIcalls } from '../../enums/APICalls';
import { Subject, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiCallService {
  serverAddress = 'http://localhost:5000/api/';
  private searchResult: Subject<any> = new Subject<any>();
  private diaplaySpinner: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(true);
  constructor(
    private http: HttpClient
  ) { }

  getPredictiveTerms(term: string): Promise<any> {
    const apiData = this.serverAddress + APIcalls.GET_PREDICTIVE_TERM + `?q=${term}`;
    return new Promise((resolve, reject) => {
      this.http.get(apiData, {
        headers: { 'Access-Control-Allow-Origin': 'http://localhost:4200'}
      }).toPromise().then(response => {
        resolve(response);
      }).catch(err => reject(err));
    });
  }

  search(query: string): Promise<any> {
    this.diaplaySpinner.next(true);
    const apiData = this.serverAddress + APIcalls.SEARCH + `?q=${query}`;
    return new Promise((resolve, reject) => {
      this.http.get(apiData, {
        headers: { 'Access-Control-Allow-Origin': ' http://localhost:4200' }
      }).toPromise().then(response => {
        this.diaplaySpinner.next(false);
        this.searchResult.next(response);
        resolve(response);
      }).catch(err => reject(err));
    });
  }

  getSearchResult() {
    return this.searchResult.asObservable();
  }

  showSpinner() {
    return this.diaplaySpinner.asObservable();
  }

}
