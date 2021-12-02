let ENV;

try {
  ENV = process.env.API_HOST }
catch {
  ENV = false
}

export default ENV || 'localhost:8000';

