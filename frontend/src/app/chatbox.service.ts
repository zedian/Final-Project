import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {Observable } from 'rxjs'
import { map, tap, catchError } from 'rxjs/operators';
@Injectable({
  providedIn: 'root'
})
export class ChatboxService {
  URL = "https://api.dialogflow.com/v1/query"
  accessToken = "b333ec6fddf8412d87ebff936359ffe7"

  APIurl = "http://localhost:4222/"
  constructor(private http: HttpClient) { }

  public sendMessage(message: string){
    let data = {
      lang: "en",
      sessionId: "111",
      query: message
    }

    let headers = new HttpHeaders().set('authorization', "Bearer "+ this.accessToken);
    //headers.append("Authorization", );
    return this.http
    .post(this.URL, data, {headers: headers});
  }

  public getEmotion(text: string){
    let data = {
      text: text
    }
    return this.http
    .post(this.APIurl, data);
  }
}
