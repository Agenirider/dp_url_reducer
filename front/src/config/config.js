let ENV;

try {
  ENV = process.env.API_HOST }
catch {
  ENV = false
}

export default ENV || 'http://localhost:8000/';

