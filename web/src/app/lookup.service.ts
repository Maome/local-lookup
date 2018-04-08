import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { Character } from './character';
import { environment } from '../environments/environment';

@Injectable()
export class LookupService {
  private baseBackendUrl = environment.apiUrl;
  constructor(private http: HttpClient) { }

  getCharacters(): Observable<Character[]> {
    return this.http.get<Character[]>(this.baseBackendUrl + "lookup")
  }

  lookupCharacters(characterArray: string[]): Observable<Character[]> {
    var charactersCSV = ""
    for(var i = 0;i < characterArray.length;i++){
        if(characterArray[i].trim().length > 0) {
            if(charactersCSV != "") {
              charactersCSV += ","
            }
            charactersCSV += characterArray[i].trim()
        }
    }
    var url = this.baseBackendUrl + "characters/information/" + charactersCSV
    return this.http.get<Character[]>(url)
  }
}
