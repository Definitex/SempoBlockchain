export enum WyreActionTypes {
  UPDATE_WYRE_STATE = "UPDATE_WYRE_STATE",

  LOAD_WYRE_EXCHANGE_RATES_REQUEST = "LOAD_WYRE_EXCHANGE_RATES_REQUEST",
  LOAD_WYRE_EXCHANGE_RATES_SUCCESS = "LOAD_WYRE_EXCHANGE_RATES_SUCCESS",
  LOAD_WYRE_EXCHANGE_RATES_FAILURE = "LOAD_WYRE_EXCHANGE_RATES_FAILURE",

  LOAD_WYRE_ACCOUNT_REQUEST = "LOAD_WYRE_ACCOUNT_REQUEST",
  LOAD_WYRE_ACCOUNT_SUCCESS = "LOAD_WYRE_ACCOUNT_SUCCESS",
  LOAD_WYRE_ACCOUNT_FAILURE = "LOAD_WYRE_ACCOUNT_FAILURE",

  CREATE_WYRE_TRANSFER_REQUEST = "CREATE_WYRE_TRANSFER_REQUEST",
  CREATE_WYRE_TRANSFER_SUCCESS = "CREATE_WYRE_TRANSFER_SUCCESS",
  CREATE_WYRE_TRANSFER_FAILURE = "CREATE_WYRE_TRANSFER_FAILURE"
}

export interface WyreState {
  wyre_rates: any | null;
  wyre_account: any | null;
  wyre_transfer: any | null;
}