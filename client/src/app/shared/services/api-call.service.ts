import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { APIcalls } from '../../enums/APICalls';

@Injectable({
  providedIn: 'root'
})
export class ApiCallService {
  serverAddress = 'http://127.0.0.1:5000/api/';
  constructor(
    private http: HttpClient
  ) { }

  getPredictiveTerms(term: string): Promise<any> {
    const apiData = this.serverAddress + APIcalls.GET_PREDICTIVE_TERM + `?q=${term}`;
    return new Promise((resolve, reject) => {
      this.http.get(apiData, {
        headers: { 'Access-Control-Allow-Origin': ' http://localhost:4200' }
      }).toPromise().then(response => {
        resolve(response);
      }).catch(err => reject(err));
    });
  }

  search(query: string, genericName?: string): Promise<any> {
    const apiData = this.serverAddress + APIcalls.SEARCH + `?q=${query}&gname=${genericName}`;
    return new Promise((resolve, reject) => {
      this.http.get(apiData).toPromise().then(response => {
        resolve(response);
      }).catch(err => reject(err));
    });
  }

}
