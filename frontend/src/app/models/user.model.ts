export interface User {
    id?: number;
    username: string;
    email: string;
}

export interface RegisterResponse {
    access_token: string;
    token_type: string;
    is_admin: boolean;
}

export interface DeleteResponse {
    detail: string;
}