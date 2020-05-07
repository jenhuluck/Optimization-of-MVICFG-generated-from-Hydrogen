void serve_static(int out_fd, int in_fd, http_request *req,
                  size_t total_size){
    char buf[256];
    if (req->offset > 0){
        sprintf(buf, "HTTP/1.1 206 Partial\r\n");
        sprintf(buf + strlen(buf), "Content-Range: bytes %lu-%lu/%lu\r\n",
                req->offset, req->end, total_size);
    } else {
        sprintf(buf, "HTTP/1.1 200 OK\r\nAccept-Ranges: bytes\r\n");
    }
    sprintf(buf + strlen(buf), "Cache-Control: no-cache\r\n");
    // sprintf(buf + strlen(buf), "Cache-Control: public, max-age=315360000\r\nExpires: Thu, 31 Dec 2037 23:55:55 GMT\r\n");

    sprintf(buf + strlen(buf), "Content-length: %lu\r\n",
            req->end - req->offset);
    sprintf(buf + strlen(buf), "Content-type: %s\r\n\r\n",
            get_mime_type(req->filename));

    writen(out_fd, buf, strlen(buf));
    off_t offset = req->offset; /* copy */
    while(offset < req->end){
        if(sendfile(out_fd, in_fd, &offset, req->end - req->offset) <= 0) {
            break;
        }
        printf("offset: %d \n\n", offset);
        close(out_fd);
        break;
    }
}
