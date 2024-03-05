import dataProviderSimpleRest from "@refinedev/simple-rest";

const API_URL = "http://localhost:8000";

const dataProvider = dataProviderSimpleRest(API_URL);

export default dataProvider;
